#pytest uses to define fixtures
#Special file
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.oauth2 import create_access_token
from app.main import app 
from app.config import settings
from app import models
from app.database import get_db, Base
#pytest --disable-warnings -v -s -x
#-x stops all testing on any failure



SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1Password@localhost:5432/fastapi-DB_test'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
#pytest.fixtures just mean that the function will be called in the test and can be passed to test function
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def getClient(session):
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()
    #run our code before we run our tests
    yield TestClient(app)
    #run our code after our test finishes
    
@pytest.fixture
def test_user2(getClient):
    user_data = {"email": "hello1234@gmail.com","password": "password123"}
    response = getClient.post("/users/",json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(getClient):
    user_data = {"email": "hello123@gmail.com","password": "password123"}
    response = getClient.post("/users/",json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})
@pytest.fixture
def authorized_client(getClient,token):
    getClient.headers = {
        **getClient.headers,
        "Authorization": f"Bearer {token}"
    }
    return getClient

@pytest.fixture 
def test_posts(test_user, session,test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "user_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "user_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "user_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "user_id": test_user2['id']
        }
    ]
    def create_post_model(post):
        return models.Post(**post)
    post_map= map(create_post_model,posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([
    #     models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #     models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
    #     models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])
    # ])
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts