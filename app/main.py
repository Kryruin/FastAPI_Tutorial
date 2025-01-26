#Switch python exe from global interpreter to the one in our Virtual Environment
#View->Command Palette
#Select the interpreter
#Check bottom right that the interpreter is from the specified Venv
#Run "FastProject\Scripts\activate.bat" in terminal and ensure that the venv name is on the left side of the prompt
#To exit venv, run "deactivate"
#(FastProject) C:\Users\Admin\Documents\Python Work\FastAPI Project>


#To Run
#########################################################################################
#Run "uvicorn <directory>.<fileName without extension>:<fastapi Instance> --reload"
#uvicorn app.main:app --reload
from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import post,user, auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#app get is a decorator to use http methods
@app.get("/",status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello  aasd World"}

