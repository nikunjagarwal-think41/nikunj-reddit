import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.main import app
from server.database import Base
from server.dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def auth_headers(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
