from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SignupSchema(BaseModel):
    name: str
    email: str
    password: str


class LoginSchema(BaseModel):
    email: str
    password: str


class ProjectSchema(BaseModel):
    name: str


class TaskSchema(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: Optional[datetime] = None
    priority: str
    assigned_to: Optional[int] = None
    project_id: int


class UpdateTaskSchema(BaseModel):
    status: str


class AssignTaskSchema(BaseModel):
    assigned_to: Optional[int] = None


class AddMemberSchema(BaseModel):
    user_id: int