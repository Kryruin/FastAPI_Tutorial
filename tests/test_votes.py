import pytest
from app import models
#pytest --disable-warnings -v -s -x tests/test_votes.py
@pytest.fixture
def test_vote(test_posts,session,test_user):
    new_vote = models.Vote(post_id=test_posts[3].id,user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
    
def test_vote_on_post(authorized_client,test_posts):
    response = authorized_client.post("/vote/", json= {"post_id":test_posts[0].id,"dir":1})
    assert response.status_code == 201
    
def test_vote_twice_post(authorized_client,test_posts,test_vote):
    response = authorized_client.post("/vote/", json= {"post_id":test_posts[3].id,"dir":1})
    assert response.status_code == 409
    
def test_delete_unvote(authorized_client,test_posts,test_vote):
    response = authorized_client.post("/vote/", json= {"post_id":test_posts[3].id,"dir":0})
    assert response.status_code == 201
    
def test_delete_vote_non_exist(authorized_client,test_posts):
    response = authorized_client.post("/vote/", json= {"post_id":test_posts[3].id,"dir":0})
    assert response.status_code == 404
    
def test_vote_post_non_exist(authorized_client,test_posts):
    response = authorized_client.post("/vote/", json= {"post_id":888888,"dir":1})
    assert response.status_code == 404
    
def test_vote_unauthorized_user(getClient,test_posts):
    response = getClient.post("/vote/", json= {"post_id":test_posts[3].id,"dir":1})
    assert response.status_code == 401