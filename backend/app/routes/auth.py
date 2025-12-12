from app.schemas.auth import UserLogin
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.auth.security import verify_password, create_access_token, create_refresh_token, get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", 
    response_model=UserOut, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
Register a new user

- Returns the created user details
""",
    responses={
        201: {"description": "User successfully registered"},
        400: {"description": "User with this email already exists"},
    }
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    TODO: Implement user registration logic
    - Check if user exists
    - Hash password
    - Create user in database
    """

    existing_user = db.scalars(select(User).where(User.email == user_data.email)).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    hashed_password = get_password_hash(user_data.password)
    
    user = User(**user_data.model_dump(), hashed_password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserOut(user)

@router.post(
    "/login", 
    response_model=str,
    summary="Login user and obtain JWT tokens",
    description="""
Login user and obtain JWT tokens
- Returns access and refresh tokens
""",
    responses={
        200: {"description": "User successfully logged in"},
        401: {"description": "Invalid email or password"},
    }
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT tokens
    """
    user = db.scalars(select(User).where(User.email == payload.email)).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return access_token


@router.post("/refresh", response_model=str)
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
