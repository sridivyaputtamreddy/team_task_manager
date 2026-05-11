
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr


class SignupSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ProjectSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class TaskSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

    description: Optional[str] = None

    due_date: Optional[datetime] = None

    priority: Literal["low", "medium", "high"]

    assigned_to: Optional[int] = None

    project_id: int


class UpdateTaskSchema(BaseModel):
    status: Literal[
        "pending",
        "in_progress",
        "completed"
    ]


class AssignTaskSchema(BaseModel):
    assigned_to: Optional[int] = None


class AddMemberSchema(BaseModel):
    user_id: int