from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime


# ========================
# USER MODEL
# ========================
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    projects = relationship(
        "ProjectMember",
        back_populates="user",
        cascade="all, delete"
    )

    assigned_tasks = relationship(
        "Task",
        back_populates="assigned_user"
    )


# ========================
# PROJECT MODEL
# ========================
class Project(Base):
    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    members = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete"
    )

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete"
    )


# ========================
# PROJECT MEMBER MODEL
# ========================
class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    role = Column(
        String(50),
        default="Member"
    )

    user = relationship(
        "User",
        back_populates="projects"
    )

    project = relationship(
        "Project",
        back_populates="members"
    )


# ========================
# TASK MODEL
# ========================
class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    due_date = Column(
        DateTime,
        nullable=True
    )

    priority = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(50),
        default="pending"
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    assigned_user = relationship(
        "User",
        back_populates="assigned_tasks"
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )