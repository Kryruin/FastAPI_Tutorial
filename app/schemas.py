from pydantic import BaseModel, EmailStr, ValidationError, ConfigDict, Field
from typing import Optional, Annotated
from datetime import datetime
# from pydantic.types import Field
#Pydantic is a library designed for data validation
#Pydantic validates the content of its properties and acts as a schema


#Explained yo
#models from models.py are mapped into the variable names of the schemas provided here
#models.py represents the ORM model that is the structure of our db's table. The pydantic model(The schemas) is a representation of that model to be used within our code for data validation and serialization
#The variable names inside MUST be the same as the variables in the models.py
class PostModelBase(BaseModel):
    title: str
    content: str
    #Default value that does not need to be in the http request
    published: bool = True
    #Optional[<type>] 
    # rating: Optional[int] = None#
    
class PostCreate(PostModelBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # model_config = ConfigDict(strict=True)
    
class Post(PostModelBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut
    # class Config:
    #     from_attributes = True
    
class PostOut(BaseModel):
    Post: Post
    votes: int

        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # model_config = ConfigDict(strict=True)



class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: str = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]
