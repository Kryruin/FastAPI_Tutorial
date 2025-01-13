
from fastapi import  Response, status, HTTPException, Depends,  APIRouter
#From . represents the current directory
from .. import models, schemas, utils
#.. means 1 dir up
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import  List

#Tags group up the requests in categories on FastAPI page
router = APIRouter(
    prefix="/users",
    tags=['Users']
    
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def CreateUser(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash password
    hashed_pwd = utils.hash(new_user.password)
    new_user.password = hashed_pwd
    #Unpacks the new_post dictionary and maps it to the model.Post with **
    user = models.User(**new_user.model_dump())
    print(user)
    db.add(user)
    db.commit()
    #Retrieve post(Kinda like using RETURNING *)
    db.refresh(user)
    return user


#If we wanna get a single post, use "/posts/{id}"
@router.get("/{id}",response_model=schemas.UserOut)
async def get_post(id: int,db: Session = Depends(get_db)):
    selectedUser = db.query(models.User).filter(models.User.id == id).first()
    if not selectedUser:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"No homie with id: {id} lelelelel")
    return  selectedUser