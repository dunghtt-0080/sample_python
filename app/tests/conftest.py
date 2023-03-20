import pytest
from typing import Dict, Generator
from fastapi.testclient import TestClient

from app.main import app
from dotenv import dotenv_values
from app.dependencies import get_db
from app.tests.utils import get_token_header
from app.tests.database import override_get_db, TestingSessionLocal


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def user_token_header(client: TestClient) -> Dict[str, str]:
    config = dotenv_values('.env')
    email = config['ADMIN_EMAIL']
    password = config['ADMIN_PASSWORD']
    return get_token_header(
        client=client, email=email, password=password
    )

app.dependency_overrides[get_db] = override_get_db