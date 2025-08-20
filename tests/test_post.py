from fastapi.testclient import TestClient

def test_create_post(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    response = client.post(
        "/api/subreddits/testsubreddit/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post"

def test_create_post_directly(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    response = client.post(
        "/api/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post", "subreddit_name": "testsubreddit"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post"

def test_get_posts(client: TestClient):
    response = client.get("/api/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_post(client: TestClient, auth_headers: dict):
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
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"

def test_update_post(client: TestClient, auth_headers: dict):
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
    response = client.put(
        f"/api/posts/{post_id}",
        headers=auth_headers,
        json={"title": "Updated Post", "content": "Updated content"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Post"
    assert response.json()["content"] == "Updated content"

def test_delete_post(client: TestClient, auth_headers: dict):
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
    response = client.delete(f"/api/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 200
