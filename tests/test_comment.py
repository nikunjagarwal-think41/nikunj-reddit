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
