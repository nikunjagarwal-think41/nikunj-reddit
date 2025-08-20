from fastapi.testclient import TestClient

def test_create_subreddit(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "testsubreddit"
    assert response.json()["description"] == "A test subreddit"

def test_get_subreddits(client: TestClient):
    response = client.get("/api/subreddits")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_subreddit(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    response = client.get("/api/subreddits/testsubreddit")
    assert response.status_code == 200
    assert response.json()["name"] == "testsubreddit"

def test_create_subreddit_existing_name(client: TestClient, auth_headers: dict):
    client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "A test subreddit"},
    )
    response = client.post(
        "/api/subreddits",
        headers=auth_headers,
        json={"name": "testsubreddit", "description": "Another test subreddit"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Subreddit with this name already exists"
