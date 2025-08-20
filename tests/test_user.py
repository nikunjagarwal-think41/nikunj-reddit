from fastapi.testclient import TestClient

def test_read_user(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    response = client.get("/api/users/testuser")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert "hashed_password" not in response.json()

def test_read_non_existent_user(client: TestClient):
    response = client.get("/api/users/nonexistentuser")
    assert response.status_code == 404
