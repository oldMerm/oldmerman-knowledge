# AGENTS.md

## Running the App

```bash
python main.py
# Runs on localhost:8000
```

## Project Structure

- `main.py` - FastAPI entry point, includes routers
- `routes/` - API route handlers (`auth.py` at `/auth/login`, `/auth/register`)
- `middleware/` - Middleware components (exception handling, response wrapper, auth)
- `services/` - Business logic services (AuthService)
- `db/` - Database connection utilities
- `db/entities/` - SQLAlchemy/Pydantic entities (User, UserStatus)
- `common/Result.py` - Generic API response wrapper (`Result.success()`, `Result.error()`)
- `utils/` - Utilities (`logger.py`, `jwt.py`)

## Key Patterns

- Use `Result[T]` from `common.Result` for API responses with automatic timestamp and code/message/data structure
- Pydantic models for request/response schemas
- Routes use `APIRouter(prefix="...")` for path prefixes
- Import module contents via package `__init__.py` exports (e.g., `from services import auth_service`)

## Module Exports

### common
- `Result` - Generic API response wrapper

### utils
- `get_logger(name)` - Custom logger
- `create_token(user_id, username)` - Create JWT token
- `verify_token(token)` - Verify JWT token
- `get_jwt_secret()` - Get JWT secret
- `TokenData` - Pydantic model for token payload

### middleware
- `register_exception_handlers(app)` - Register exception handlers
- `ResponseWrapperMiddleware` - Wrap responses with Result
- `AuthMiddleware` - JWT authentication middleware

### services
- `AuthService` - Authentication service class
- `auth_service` - Singleton instance

### db
- `get_connection()` - Get database connection
- `close_connection(conn)` - Close database connection
- `init_db()` - Initialize database

### db.entities
- `User` - User entity model
- `UserStatus` - User status enum

## Dependencies

- FastAPI, Pydantic, psycopg (PostgreSQL), psycopg_pool, python-dotenv, JWT, bcrypt, LangChain, LangGraph

## Notes

- `.env` file requires: `DATABASE_URL`, `OPENAI_API_KEY`, `JWT_SECRET`, `ENVIRONMENT` (development/production/test)
- No test/lint/typecheck tooling configured