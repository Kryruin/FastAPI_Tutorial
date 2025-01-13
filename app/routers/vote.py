from fastapi import  Response, status, HTTPException, Depends, APIRouter
#From . represents the current directory
from .. import models, schemas, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not postQuery.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"No post with id: {vote.post_id} ")
    
    
    voteQuery = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    foundvote = voteQuery.first()
    
    if (vote.dir == 1):
        if foundvote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted hehe")
        voteObj = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(voteObj)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not foundvote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"vote is missing huhu")
        voteQuery.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}