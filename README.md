# FastAPI Demo Application

A REST API demonstrating FastAPI capabilities with JWT authentication, CRUD operations, and best practices.

## Features

- **JWT Authentication** - OAuth2 password flow with Bearer tokens
- **User Management** - Complete CRUD operations for users
- **Task Management** - Task creation, updates, and completion tracking
- **Pydantic Validation** - Strong request/response validation
- **Pagination & Filtering** - Query parameters for efficient data retrieval
- **OpenAPI Documentation** - Auto-generated interactive API docs

## Tech Stack

- FastAPI
- Pydantic
- JWT (PyJWT)
- Python 3.12
- Docker & Docker Compose

## Quick Start

### Local Development

1. Clone the repository
```bash
git clone <repo-url>
cd fastapi-demo-api
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
uvicorn app.main:app --reload
```

4. Open http://localhost:8000/docs to see the interactive API documentation

### Docker

```bash
docker-compose up --build
```

Access the API at http://localhost:8000

### Configuration

The project includes a working `.env` file with demo credentials. For production or to add/modify users:

```env
SECRET_KEY=your-secure-secret-key-here
DEMO_USERS={"admin": "admin123", "user": "user123", "newuser": "pass456"}
```

**Format**: JSON object with username-password pairs

**Note**: In production, use a proper database with hashed passwords instead of plain text credentials.

## API Endpoints

### Authentication
- `POST /token/` - Get JWT token (OAuth2 password flow)

### Users
- `POST /users/` - Create new user
- `GET /users/` - List users (with pagination)
- `GET /users/{id}` - Get user by ID
- `DELETE /users/{id}` - Delete user

### Tasks
- `POST /tasks/` - Create new task
- `GET /tasks/` - List tasks (with filtering & pagination)
- `PUT /tasks/{id}` - Update task
- `PATCH /tasks/{id}/complete` - Mark task as completed
- `DELETE /tasks/{id}` - Delete task

## Documentation

Access interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication Flow

1. Get token via `POST /token/` with username and password in form data
2. Use token in `Authorization: Bearer <token>` header for protected endpoints

### Demo Credentials

- **Admin**: username: `admin`, password: `admin123`
- **User**: username: `user`, password: `user123`

## Example Usage

### Get JWT Token
```bash
curl -X POST "http://localhost:8000/token/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Create User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Create Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the FastAPI demo"
  }'
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── auth.py          # JWT authentication logic
│   └── config.py        # Configuration and settings
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                 # Environment variables (not in git)
└── README.md
```
