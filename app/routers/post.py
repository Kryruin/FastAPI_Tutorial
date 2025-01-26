from fastapi import  Response, status, HTTPException, Depends, APIRouter
#From . represents the current directory
from .. import models, schemas, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import  List, Optional

#Tags group up the requests in categories on FastAPI page
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/",response_model=List[schemas.Post])
#,response_model=List[schemas.PostOut]
# @router.get("/")
@router.get("/",response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,skip:int = 0, search: Optional[str] = ""):
    # results = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = (
        db.query(
            models.Post, 
            func.count(models.Vote.post_id).label("votes")
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return results



#If we wanna get a single post, use "/posts/{id}"
@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # selectedPost = db.query(models.Post).filter(models.Post.id == id).first()
    selectedPost = db.query(
            models.Post, 
            func.count(models.Vote.post_id).label("votes")
        ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not selectedPost:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"No post with id: {id} lelelelel")
    # if selectedPost.user_id != current_user.id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail= f"Post {id} isn't yours to get homie")
    return  selectedPost


#CRUD STUFF

#Parameter takes the body of the post request
#Title str
#Depends(oauth2.get_current_user) ensures that the API endpoint requires a token
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createPosts(new_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #Unpacks the new_post dictionary and maps it to the model.Post with **
    post = models.Post(user_id = current_user.id , **new_post.model_dump())
    print(post)
    db.add(post)
    db.commit()
    #Retrieve post(Kinda like using RETURNING *)
    db.refresh(post)
    return post

#Typically when data is deleted, we don't send data back (204 response)
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePosts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    postToRemoveQuery = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""Delete from posts where id = %s Returning* """, (str(id)))
    # postToRemove = cursor.fetchone()
    if postToRemoveQuery.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"No post with id: {id} to be deleted")
    if postToRemoveQuery.first().user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail= f"Post {id} isn't yours to delete homie")
        
    #commit the change to the database
    # conn.commit()
    postToRemoveQuery.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Typically when data is deleted, we don't send data back
@router.put("/{id}",response_model=schemas.Post)
def updatePost(id: int, new_post: schemas.PostModelBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    postToUpdateQuery = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s Where id = %s RETURNING *""", (new_post.title,new_post.content, new_post.published,str(id)))
    # postToUpdate = cursor.fetchone()
    # conn.commit()
    if not postToUpdateQuery.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"No post with id: {id} to be updated")
    if postToUpdateQuery.first().user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail= f"Post {id} isn't yours to update homie")
    postToUpdateQuery.update(new_post.model_dump(),synchronize_session=False)
    db.commit()
    return postToUpdateQuery.first()