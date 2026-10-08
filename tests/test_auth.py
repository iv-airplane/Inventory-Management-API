from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register", json={"email": "a@a.com", "password": "pw12345"}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["email"] == "a@a.com"
    assert data["role"] == "user"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client: TestClient):
    client.post("/auth/register", json={"email": "a@a.com", "password": "pw12345"})
    response = client.post(
        "/auth/register", json={"email": "a@a.com", "password": "different"}
    )

    assert response.status_code == 409


def test_login_success(client: TestClient):
    client.post("/auth/register", json={"email": "a@a.com", "password": "pw12345"})

    response = client.post(
        "/auth/login", data={"username": "a@a.com", "password": "pw12345"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_wrong_password(client: TestClient):
    client.post("/auth/register", json={"email": "a@a.com", "password": "pw12345"})

    response = client.post(
        "/auth/login", data={"username": "a@a.com", "password": "wrong"}
    )

    assert response.status_code == 401


def test_login_unknown_email(client: TestClient):
    response = client.post(
        "/auth/login", data={"username": "nobody@a.com", "password": "pw12345"}
    )

    assert response.status_code == 401
