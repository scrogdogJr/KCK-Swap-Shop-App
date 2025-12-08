from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, User

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    TODO: Implement user registration logic
    - Check if user exists
    - Hash password
    - Create user in database
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration endpoint not implemented"
    )


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login user and return JWT tokens
    TODO: Implement login logic
    - Verify user credentials
    - Generate access and refresh tokens
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login endpoint not implemented"
    )


@router.post("/refresh", response_model=Token)
def refresh_token(db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    TODO: Implement token refresh logic
    - Verify refresh token
    - Generate new access token
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token endpoint not implemented"
    )
