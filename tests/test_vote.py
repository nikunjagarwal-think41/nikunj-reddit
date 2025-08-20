from fastapi.testclient import TestClient

def test_vote_on_post(client: TestClient, auth_headers: dict):
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

    # Upvote the post
    response = client.post(
        f"/api/posts/{post_id}/vote",
        headers=auth_headers,
        json={"vote_type": "upvote"},
    )
    assert response.status_code == 200
    assert response.json()["vote_type"] == "upvote"

    # Downvote the post
    response = client.post(
        f"/api/posts/{post_id}/vote",
        headers=auth_headers,
        json={"vote_type": "downvote"},
    )
    assert response.status_code == 200
    assert response.json()["vote_type"] == "downvote"

    # Remove the vote
    response = client.post(
        f"/api/posts/{post_id}/vote",
        headers=auth_headers,
        json={"vote_type": "downvote"},
    )
    assert response.status_code == 204