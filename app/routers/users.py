from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

from app.service import user as UserService
from app.schemas.user import User, UserCreate
from app.dependencies import get_db, get_current_active_user, is_admin

router = APIRouter(
    prefix="/api/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=User)
def http_create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(is_admin)):
    db_user = UserService.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return UserService.create_user(db=db, user=user)

@router.get("/", response_model=list[User])
def http_read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(is_admin)):
    users = UserService.get_users(db, skip=skip, limit=limit)

    return users

@router.get("/me", response_model=User)
def http_read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=User)
def http_read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permission")

    db_user = UserService.get_user_by_id(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
