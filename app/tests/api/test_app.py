from dotenv import dotenv_values
from fastapi.testclient import TestClient

config = dotenv_values('.env')
email = config['ADMIN_EMAIL']
password = config['ADMIN_PASSWORD']

def test_read_main(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_init_db(client: TestClient) -> None:
    response = client.get("/init_db")
    assert response.status_code == 200


def test_user_login_successful(client: TestClient) -> None:
    client.headers["content-type"] = "application/x-www-form-urlencoded"
    login_data = {
        "username": email,
        "password": password,
    }
    res = client.post('/token', data=login_data)
    assert res.status_code == 200
    token = res.json().get("access_token")
    assert "token_type" in res.json()
    assert res.json().get("token_type") == "bearer"


def test_user_login_fail(client: TestClient) -> None:
    client.headers["content-type"] = "application/x-www-form-urlencoded"
    login_data = {
        "username": email,
        "password": "wrong",
    }
    res = client.post('/token', data=login_data)
    assert "access_token" not in res.json()
