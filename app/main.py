from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from .auth import create_jwt_token, verify_jwt_token, authenticate_user
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="FastAPI Demo API",
    description="A REST API demonstrating FastAPI capabilities with JWT authentication",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


users_db = []
tasks_db = []
user_id_counter = 1
task_id_counter = 1


@app.post("/token/", tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_jwt_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/", tags=["General"])
async def root():
    return {
        "message": "FastAPI Demo API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(
    user: UserCreate,
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)

    global user_id_counter

    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    new_user = User(
        id=user_id_counter,
        username=user.username,
        email=user.email
    )
    users_db.append(new_user.dict())
    user_id_counter += 1

    return new_user


@app.get("/users/", response_model=List[User], tags=["Users"])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)
    return users_db[skip:skip + limit]


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(
    user_id: int,
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)

    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(
    user_id: int,
    token: str = Depends(oauth2_scheme),
):
    global users_db
    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    users_db.pop(user_index)
    return None


@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(
    task: TaskCreate,
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)

    global task_id_counter

    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description
    )
    tasks_db.append(new_task.dict())
    task_id_counter += 1

    return new_task


@app.get("/tasks/", response_model=List[Task], tags=["Tasks"])
async def get_tasks(
    completed: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)

    filtered_tasks = tasks_db
    if completed is not None:
        filtered_tasks = [t for t in tasks_db if t["completed"] == completed]

    return filtered_tasks[skip:skip + limit]


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(
    task_id: int,
    task: TaskCreate,
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)

    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    tasks_db[task_index]["title"] = task.title
    tasks_db[task_index]["description"] = task.description

    return tasks_db[task_index]


@app.patch("/tasks/{task_id}/complete", response_model=Task, tags=["Tasks"])
async def mark_task_complete(
    task_id: int,
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)

    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    tasks_db[task_index]["completed"] = True

    return tasks_db[task_index]


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(
    task_id: int,
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)

    global tasks_db
    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    tasks_db.pop(task_index)
    return None
