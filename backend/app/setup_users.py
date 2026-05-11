#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.dirname(__file__))

from database import SessionLocal
from models import User, Project, ProjectMember
from auth import hash_password


def create_test_users():
    db = SessionLocal()

    try:
        # ========================
        # TEST USERS
        # ========================
        users_data = [
            {
                "name": "Team Lead",
                "email": "lead@example.com",
                "password": "password123",
                "role": "Admin"
            },
            {
                "name": "Developer 1",
                "email": "dev1@example.com",
                "password": "password123",
                "role": "Member"
            },
            {
                "name": "Developer 2",
                "email": "dev2@example.com",
                "password": "password123",
                "role": "Member"
            },
            {
                "name": "QA Tester",
                "email": "qa@example.com",
                "password": "password123",
                "role": "Member"
            },
        ]

        created_users = []

        # ========================
        # CREATE USERS
        # ========================
        for user_data in users_data:

            existing = db.query(User).filter(
                User.email == user_data["email"]
            ).first()

            if existing:
                print(
                    f"User already exists: "
                    f"{user_data['email']}"
                )

                created_users.append(existing)
                continue

            user = User(
                name=user_data["name"],
                email=user_data["email"],
                password=hash_password(
                    user_data["password"]
                )
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            created_users.append(user)

            print(
                f"Created user: "
                f"{user.name} ({user.email})"
            )

        # ========================
        # FIND PROJECT
        # ========================
        project = db.query(Project).first()

        if not project:
            print(
                "No projects found. "
                "Please create a project first."
            )
            return

        print(f"\nUsing project: {project.name}")

        # ========================
        # ADD USERS TO PROJECT
        # ========================
        for i, user in enumerate(created_users):

            existing_membership = db.query(
                ProjectMember
            ).filter(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == user.id
            ).first()

            if existing_membership:
                print(
                    f"{user.name} is already "
                    f"a member of {project.name}"
                )
                continue

            role = (
                "Admin"
                if i == 0
                else "Member"
            )

            membership = ProjectMember(
                project_id=project.id,
                user_id=user.id,
                role=role
            )

            db.add(membership)
            db.commit()

            print(
                f"Added {user.name} "
                f"as {role} "
                f"to project {project.name}"
            )

        # ========================
        # SUCCESS
        # ========================
        print("\n✅ Test users setup complete!")

        print("\nLogin credentials:")

        for user_data in users_data:
            print(
                f"- {user_data['name']}: "
                f"{user_data['email']} / "
                f"{user_data['password']}"
            )

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    create_test_users()