from fastapi.testclient import TestClient

def test_create_comment(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    post_response = client.post(
        "/api/subreddits/testsubreddit/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    response = client.post(
        f"/api/posts/{post_id}/comments",
        headers=auth_headers,
        json={"content": "This is a test comment"},
    )
    assert response.status_code == 200
    assert response.json()["content"] == "This is a test comment"

def test_get_comments_for_post(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    post_response = client.post(
        "/api/subreddits/testsubreddit/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    client.post(
        f"/api/posts/{post_id}/comments",
        headers=auth_headers,
        json={"content": "This is a test comment"},
    )
    response = client.get(f"/api/posts/{post_id}/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_update_comment(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    post_response = client.post(
        "/api/subreddits/testsubreddit/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        headers=auth_headers,
        json={"content": "This is a test comment"},
    )
    comment_id = comment_response.json()["id"]
    response = client.put(
        f"/api/comments/{comment_id}",
        headers=auth_headers,
        json="This is an updated comment",
    )
    assert response.status_code == 200
    assert response.json()["content"] == "This is an updated comment"

def test_delete_comment(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    post_response = client.post(
        "/api/subreddits/testsubreddit/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        headers=auth_headers,
        json={"content": "This is a test comment"},
    )
    comment_id = comment_response.json()["id"]
    response = client.delete(f"/api/comments/{comment_id}", headers=auth_headers)
    assert response.status_code == 200

def test_update_comment_not_author(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    post_response = client.post(
        "/api/subreddits/testsubreddit/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        headers=auth_headers,
        json={"content": "This is a test comment"},
    )
    comment_id = comment_response.json()["id"]

    # Create a new user and get their auth headers
    client.post(
        "/api/auth/register",
        json={"username": "testuser2", "email": "test2@example.com", "password": "password"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "test2@example.com", "password": "password"},
    )
    auth_headers2 = {"Authorization": f"Bearer {response.json()['access_token']}"}

    response = client.put(
        f"/api/comments/{comment_id}",
        headers=auth_headers2,
        json="This is an updated comment",
    )
    assert response.status_code == 403

def test_delete_comment_not_author(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    post_response = client.post(
        "/api/subreddits/testsubreddit/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        headers=auth_headers,
        json={"content": "This is a test comment"},
    )
    comment_id = comment_response.json()["id"]

    # Create a new user and get their auth headers
    client.post(
        "/api/auth/register",
        json={"username": "testuser2", "email": "test2@example.com", "password": "password"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "test2@example.com", "password": "password"},
    )
    auth_headers2 = {"Authorization": f"Bearer {response.json()['access_token']}"}

    response = client.delete(f"/api/comments/{comment_id}", headers=auth_headers2)
    assert response.status_code == 403
