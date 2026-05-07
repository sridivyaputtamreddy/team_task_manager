#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import SessionLocal, Base, engine
from models import User, Project, ProjectMember
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_test_users():
    db = SessionLocal()

    try:
        # Create test users
        users_data = [
            {"name": "Team Lead", "email": "lead@example.com", "password": "password123", "role": "Admin"},
            {"name": "Developer 1", "email": "dev1@example.com", "password": "password123", "role": "Member"},
            {"name": "Developer 2", "email": "dev2@example.com", "password": "password123", "role": "Member"},
            {"name": "QA Tester", "email": "qa@example.com", "password": "password123", "role": "Member"},
        ]

        created_users = []
        for user_data in users_data:
            # Check if user already exists
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"User {user_data['email']} already exists")
                created_users.append(existing)
                continue

            user = User(
                name=user_data["name"],
                email=user_data["email"],
                password=hash_password(user_data["password"])
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            created_users.append(user)
            print(f"Created user: {user.name} ({user.email})")

        # Get the first project (created earlier)
        project = db.query(Project).first()
        if not project:
            print("No projects found. Please create a project first.")
            return

        print(f"Using project: {project.name}")

        # Add users to project with appropriate roles
        for i, user in enumerate(created_users):
            # Check if membership already exists
            existing_membership = db.query(ProjectMember).filter(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == user.id
            ).first()

            if existing_membership:
                print(f"User {user.name} is already a member of {project.name}")
                continue

            # First user (Team Lead) gets Admin role, others get Member
            role = "Admin" if i == 0 else "Member"

            membership = ProjectMember(
                project_id=project.id,
                user_id=user.id,
                role=role
            )
            db.add(membership)
            db.commit()
            print(f"Added {user.name} as {role} to project {project.name}")

        print("\n✅ Test users setup complete!")
        print("\nLogin credentials:")
        for user_data in users_data:
            print(f"- {user_data['name']}: {user_data['email']} / {user_data['password']}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()