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

def test_vote_on_comment(client: TestClient, auth_headers: dict):
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

    # Upvote the comment
    response = client.post(
        f"/api/comments/{comment_id}/vote",
        headers=auth_headers,
        json={"vote_type": "upvote"},
    )
    assert response.status_code == 200
    assert response.json()["vote_type"] == "upvote"

    # Downvote the comment
    response = client.post(
        f"/api/comments/{comment_id}/vote",
        headers=auth_headers,
        json={"vote_type": "downvote"},
    )
    assert response.status_code == 200
    assert response.json()["vote_type"] == "downvote"

    # Remove the vote
    response = client.post(
        f"/api/comments/{comment_id}/vote",
        headers=auth_headers,
        json={"vote_type": "downvote"},
    )
    assert response.status_code == 204
