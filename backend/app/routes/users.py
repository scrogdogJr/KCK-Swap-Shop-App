from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.models.user import User as UserModel
from app.auth.dependencies import require_admin, require_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_admin)
):
    """
    Retrieve users (admin only)
    TODO: Implement user retrieval logic
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get users endpoint not implemented"
    )


@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: UserModel = Depends(require_user)):
    """
    Get current user information
    """
    return current_user


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_user)
):
    """
    Get user by ID
    TODO: Implement user retrieval by ID
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get user endpoint not implemented"
    )


@router.put("/me", response_model=UserOut)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_user)
):
    """
    Update current user
    TODO: Implement user update logic
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Update user endpoint not implemented"
    )


@router.delete("/{user_id}", response_model=UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_admin)
):
    """
    Delete user (admin only)
    TODO: Implement user deletion logic
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Delete user endpoint not implemented"
    )
