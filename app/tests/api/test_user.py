import pytest
from typing import Dict

from fastapi.testclient import TestClient


def test_get_users_me(
    client: TestClient, user_token_header: Dict[str, str]
) -> None:
    r = client.get("/api/users/me", headers=user_token_header)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_admin"] is True
