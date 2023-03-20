from httpx import AsyncClient
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

from app.service import user as UserService
from app.schemas.user import User, UserCreate
from app.dependencies import get_db, get_current_active_user, is_admin

router = APIRouter(
    prefix="/api/external",
    tags=["External"],
    responses={404: {"description": "Not found"}},
)

client = AsyncClient()

@router.get("/users")
async def get_external_users():
    result = await client.get("https://reqres.in/api/users")
    return result.text


@router.put("/users/{user_id}")
async def put_external_users(user_id: int):
    input_data = {
        "name": "morpheus",
        "job": "zion resident",
    }
    result = await client.put("https://reqres.in/api/users/" + str(user_id), params = input_data)
    return result.text


@router.post("/users")
async def post_external_users():
    input_data = {
        "name": "morpheus",
        "job": "leader",
    }
    result = await client.post("https://reqres.in/api/users", params = input_data)
    return result.text


@router.delete("/users/{user_id}")
async def delete_external_users(user_id: int):
    result = await client.put("https://reqres.in/api/users/" + str(user_id))
    return result.text
