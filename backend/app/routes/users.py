from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.models.user import User
from app.auth.dependencies import require_admin, require_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "", 
    response_model=List[UserOut],
    summary="Retrieve users (admin only)",
    description="""
    Retrieve a list of users. This endpoint is restricted to admin users only.
    - **Admin Access Only***: Only users with admin privileges can access this endpoint.
    - Returns a list of user objects.
    """,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of users retrieved successfully"},
        401: {"description": "Unauthorized - Admin access required"}
    }
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Retrieve users (admin only)
    """
    users = db.scalars(select(User)).all()

    return [UserOut(
        id=user.id,
        email=user.email,
        name=user.name,
        phone=user.phone,
        parish=user.parish,
        admin=user.admin
    ) for user in users]

@router.get(
        "/me", 
        response_model=UserOut,
        summary="Get current user information",
        description="""
        Retrieve information about the currently authenticated user.
        - **Authentication Required**: The user must be authenticated to access this endpoint.
        - Returns the user's details including email, name, phone, parish, and admin status.
        """,
        status_code=status.HTTP_200_OK,
        responses={
            200: {"description": "Current user information retrieved successfully"},
            401: {"description": "Unauthorized - Authentication required"}
        }
)
def get_current_user_info(current_user: User = Depends(require_user)):
    """
    Get current user information
    """
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        phone=current_user.phone,
        parish=current_user.parish,
        admin=current_user.admin
    )

@router.get(
    "/{user_id}", 
    response_model=UserOut,
    summary="Get user by ID (admin only)",
    description="""
    Retrieve a user by their ID. This endpoint is restricted to admin users only.
    - **Admin Access Only**: Only users with admin privileges can access this endpoint.
    - Returns the user object corresponding to the provided ID.
    """,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User retrieved successfully"},
        404: {"description": "User not found"},
        401: {"description": "Unauthorized - Admin access required"}
    }
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get user by ID (admin only)
    """

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserOut(
        id=user.id,
        email=user.email,
        name=user.name,
        phone=user.phone,
        parish=user.parish,
        admin=user.admin
    )

@router.put(
    "/me", 
    response_model=UserOut,
    summary="Update current user information",
    description="""
    Update information for the currently authenticated user.
    - **Authentication Required**: The user must be authenticated to access this endpoint.
    - Accepts fields to update such as email, username, phone, parish, and admin status.
    - Returns the updated user object.
    """,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Current user information updated successfully"},
        401: {"description": "Unauthorized - Authentication required"}
    }
)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    """
    Update current user information
    """

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)

    return UserOut(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        phone=current_user.phone,
        parish=current_user.parish,
        admin=current_user.admin
    )


@router.delete(
    "/{user_id}", 
    response_model=UserOut,
    summary="Delete user (admin only)",
    description="""
    Delete a user by their ID. This endpoint is restricted to admin users only.
    - **Admin Access Only**: Only users with admin privileges can access this endpoint.
    - Deletes the user corresponding to the provided ID.
    """,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
        401: {"description": "Unauthorized - Admin access required"}
    }
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete user (admin only)
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
