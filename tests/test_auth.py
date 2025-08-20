from fastapi.testclient import TestClient

def test_register(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_register_existing_email(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser2", "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_incorrect_credentials(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"