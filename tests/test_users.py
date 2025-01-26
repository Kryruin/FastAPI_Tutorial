from app import schemas
# from .database import getClient, session
import pytest
from jose import jwt
from app.config import settings



#pytest --disable-warnings -v -s -x
#-x stops all testing on any failure
# def test_root(getClient):
#     response = getClient.get("/")
#     print(response.json().get('message'))
#     assert response.json().get('message') == "Hello  aasd World"
#     assert response.status_code == 200
    
def test_create_user(getClient):
    response = getClient.post("/users/",json={"email": "hello123@gmail.com","password": "password123"})
    temp = schemas.UserOut(**response.json())
    assert response.json().get("email") == "hello123@gmail.com"
    assert response.status_code == 201
    

def test_login_user(getClient, test_user):
    # requires form data instead of json
    response = getClient.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**response.json())

    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    # from the token that was decoded, get the "users_id" key from the paylod
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 403),
    ('sanjeev@gmail.com', None, 403)
])
def test_incorrect_login(getClient,test_user, email, password, status_code):
    # requires form data instead of json
    response = getClient.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    # assert response.json().get('detail') == "Invalid Credentials"