# FastAPI JWT Auth Boilerplate

A FastAPI application boilerplate with JWT authentication structure and PostgreSQL database using SQLAlchemy.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # App configuration
│   ├── database.py          # Database session and engine
│   ├── security.py          # JWT and password utilities
│   ├── dependencies.py      # Auth dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token.py
│   └── routes/              # API routes
│       ├── __init__.py
│       ├── auth.py
│       └── users.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
copy .env.example .env
```

Update the following in `.env`:
- `POSTGRES_*`: Your PostgreSQL connection details
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `BACKEND_CORS_ORIGINS`: Your frontend URLs

### 3. Set Up PostgreSQL Database

Ensure PostgreSQL 16 is installed and create a database:

```sql
CREATE DATABASE your_database_name;
```

### 4. Run the Application

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Folder Structure

### `/models` - Database Models
Contains SQLAlchemy ORM models that define the database schema.
- `user.py`: User model with authentication fields

### `/schemas` - Pydantic Schemas
Contains Pydantic models for request/response validation.
- `user.py`: User-related schemas (UserCreate, UserUpdate, User, UserInDB)
- `token.py`: JWT token schemas (Token, TokenPayload)

### `/routes` - API Routes
Contains FastAPI route handlers organized by resource.
- `auth.py`: Authentication endpoints (register, login, refresh)
- `users.py`: User management endpoints

## Authentication Implementation

The boilerplate includes the structure for JWT authentication but endpoints are not fully implemented. To complete the implementation:

1. **Register Endpoint** (`routes/auth.py`):
   - Validate user data
   - Check if user already exists
   - Hash password using `get_password_hash`
   - Create user in database

2. **Login Endpoint** (`routes/auth.py`):
   - Validate credentials
   - Verify password using `verify_password`
   - Generate tokens using `create_access_token` and `create_refresh_token`

3. **User Dependencies** (`dependencies.py`):
   - Implement `get_current_user` to decode JWT and retrieve user

## Database Migrations (Optional)

To use Alembic for database migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Features

- ✅ FastAPI application structure
- ✅ JWT token utilities (access and refresh tokens)
- ✅ Password hashing with bcrypt
- ✅ SQLAlchemy models and database setup
- ✅ Pydantic schemas for validation
- ✅ CORS middleware
- ✅ PostgreSQL connection
- ✅ API versioning (v1)
- ✅ User model with timestamps
- ✅ Organized folder structure (models, schemas, routes)
- ⏳ Authentication endpoints (structure ready)
- ⏳ Protected routes (structure ready)

## Next Steps

1. Implement the TODO items in:
   - `routes/auth.py`
   - `routes/users.py`
   - `dependencies.py`

2. Add CRUD operations for users in a service layer

3. Set up database migrations with Alembic

4. Add additional models and endpoints as needed

5. Implement proper error handling and logging

6. Add unit tests
