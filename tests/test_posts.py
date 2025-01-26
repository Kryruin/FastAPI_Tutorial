from typing import List
from app import schemas
import pytest
#pytest --disable-warnings -v -s -x tests/test_posts.py
def test_get_all_posts(authorized_client,test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.Postout(**post)
    posts_map = map(validate,response.json())
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_get_all_post(getClient,test_posts):
    response = getClient.get("/posts/")
    assert response.status_code == 401
def test_unauthorized_get_one_post(getClient,test_posts):
    response = getClient.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_get_one_post(authorized_client,test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

#parametrize allows for multiple variations of parameters to be tested
@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content,
                                                "published": published})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']

def test_unauthorized_create_post(getClient,test_posts):
    response = getClient.post(f"/posts/", json={"title": "title", "content": "content"})
    assert response.status_code == 401
    
def test_unauthorized_delete_post(getClient,test_posts):
    response = getClient.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204
    
def test_delete_post_non_exists(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/9999999")
    assert response.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user,test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}",json=data)
    assert response.status_code == 403

def test_unauthorized_update_post(getClient,test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = getClient.put(f"/posts/{test_posts[0].id}",json=data)
    assert response.status_code == 401
    
def test_update_post_non_exists(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/posts/9999999",json=data)
    assert response.status_code == 404