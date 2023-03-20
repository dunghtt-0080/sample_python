import pytest
from typing import Generator
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas.user import UserCreate
from app.service import user as UserService
from app.tests.utils import random_email, random_lower_string

def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_admin=False)
    user = UserService.create_user(db, user=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_active=True,  is_admin=False)
    user = UserService.create_user(db, user=user_in)
    is_active = UserService.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_active=False, is_admin=False)
    user = UserService.create_user(db, user=user_in)
    is_active = UserService.is_active(user)
    assert is_active


def test_check_if_user_is_admin(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_admin=True)
    user = UserService.create_user(db, user=user_in)
    is_superuser = UserService.is_admin(user)
    assert is_superuser is True


def test_check_if_user_is_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, is_admin=False)
    user = UserService.create_user(db, user=user_in)
    is_admin = UserService.is_admin(user)
    assert is_admin is False


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_admin=True)
    user = UserService.create_user(db, user=user_in)
    user_2 = UserService.get_user_by_id(db, user_id=user.id)
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)

