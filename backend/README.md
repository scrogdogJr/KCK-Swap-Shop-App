# KCK Swap Shop - Backend

FastAPI backend with JWT authentication and SQLAlchemy ORM.

## Prerequisites

- Python 3.13+
- pip (Python package manager)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "KCK Swap Shop/backend"
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you encounter bcrypt compatibility issues, install this specific version:
```bash
pip install bcrypt==4.0.1
```

### 4. Configure Environment

Create a `.env` file in the backend directory:

```env
# Database Configuration
USE_SQLITE=true
SQLITE_DATABASE_URL=sqlite:///./kck_swap_shop.db
DATABASE_URL=postgresql://user:password@localhost:5432/kck_swap_shop

# JWT Settings
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=KCK Swap Shop API
```

**Development Note:** For development, keep `USE_SQLITE=true` to use the portable SQLite database.

### 5. Initialize Database

Seed the database with test accounts:

```bash
python seed_database.py
```

This creates:
- **Admin User:** admin@example.com / admin123
- **Regular Users:** john@example.com, jane@example.com / password123

### 6. Start Development Server

```bash
python run_dev.py
```

The server will start at **http://localhost:8000**

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── auth/
│   │   ├── security.py      # JWT and password utilities
│   │   └── dependencies.py  # Auth dependencies
│   ├── core/
│   │   └── config.py        # Application settings
│   ├── models/
│   │   ├── user.py          # SQLAlchemy models
│   │   └── parish.py
│   ├── schemas/
│   │   ├── auth.py          # Pydantic schemas
│   │   └── user.py
│   └── routes/
│       ├── auth.py          # Authentication endpoints
│       └── users.py         # User management endpoints
├── tests/                   # Unit tests (170+ tests)
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── seed_database.py         # Database seeding script
└── run_dev.py              # Development server runner
```

## Running Tests

Run the test suite with pytest:

```bash
pytest
```

Run with coverage report:

```bash
pytest --cov=app --cov-report=html
```

## Database Options

### SQLite (Development)
- Portable, file-based database
- Perfect for development and testing
- No additional setup required
- Set `USE_SQLITE=true` in `.env`

### PostgreSQL (Production)
- For production deployments
- Install PostgreSQL 16
- Update `DATABASE_URL` in `.env`
- Set `USE_SQLITE=false`

## Test Accounts

After running `seed_database.py`:

| Role    | Email               | Password    |
|---------|---------------------|-------------|
| Admin   | admin@example.com   | admin123    |
| User    | john@example.com    | password123 |
| User    | jane@example.com    | password123 |

## Available Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/me` - Delete current user

## Troubleshooting

### bcrypt Compatibility Issues
If you see errors about bcrypt version detection:
```bash
pip install bcrypt==4.0.1
```

### Database Already Seeded
If `seed_database.py` reports users already exist, delete the database file:
```bash
rm kck_swap_shop.db  # Linux/macOS
del kck_swap_shop.db  # Windows
```

### Port Already in Use
If port 8000 is busy, modify `run_dev.py` to use a different port:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

## Development

The development server runs with auto-reload enabled. Any changes to Python files will automatically restart the server.

### Adding New Dependencies

1. Install the package: `pip install package-name`
2. Update requirements: `pip freeze > requirements.txt`

## Security Notes

⚠️ **Important for Production:**
- Change `SECRET_KEY` to a strong random value
- Set `USE_SQLITE=false` and use PostgreSQL
- Enable HTTPS
- Configure CORS properly in `main.py`
- Use environment variables, never commit `.env` file

## Features

- ✅ FastAPI application structure
- ✅ JWT token utilities (access and refresh tokens)
- ✅ Password hashing with bcrypt
- ✅ SQLAlchemy 2.0 models and database setup
- ✅ Pydantic v2 schemas for validation
- ✅ CORS middleware configured
- ✅ SQLite/PostgreSQL support
- ✅ API versioning (v1)
- ✅ User model with timestamps
- ✅ Organized folder structure (models, schemas, routes, auth)
- ✅ Comprehensive test suite (170+ tests)
- ✅ Database seeding script
- ⏳ Authentication endpoints (structure ready, needs implementation)

## Support

For issues or questions, please open an issue in the repository
