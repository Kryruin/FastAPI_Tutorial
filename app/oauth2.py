from jose import JWTError,jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#Requires 
#Secret_Key
#Algorithm
#Expiration Time
# SECRET_KEY = "86b4c0ee0c96554d406e78e972d4b778c17d1f606e350354189098a3d8295976"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    toEncode = data.copy()
    expireTime = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expireTime})
    print(f"Expiration time: {expireTime}")

    encoded_jwt = jwt.encode(toEncode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:    
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms= [settings.ALGORITHM])
        #from the token that was decoded, get the "users_id" key from the paylod
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token= verify_access_token(token=token,credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
    