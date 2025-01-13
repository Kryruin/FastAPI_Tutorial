from  fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import oauth2, schemas, models, utils


router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_credetentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credetentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    #Check password hash
    if not utils.verify(user_credetentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
        