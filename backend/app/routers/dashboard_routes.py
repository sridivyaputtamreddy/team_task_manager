from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Task, User, ProjectMember, Project
from dependencies import get_current_user
from datetime import datetime

router = APIRouter(prefix="/dashboard")


def _is_project_member(db: Session, user: User, project_id: int):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    project_id: int = None
):
    if project_id:
        membership = _is_project_member(db, user, project_id)
        if not membership:
            raise HTTPException(status_code=403, detail="Not a member of this project")

        if membership.role == "Admin":
            query = db.query(Task).options(joinedload(Task.assigned_user)).filter(Task.project_id == project_id)
        else:
            query = db.query(Task).options(joinedload(Task.assigned_user)).filter(
                Task.project_id == project_id,
                Task.assigned_to == user.id
            )
    else:
        query = db.query(Task).options(joinedload(Task.assigned_user)).filter(Task.assigned_to == user.id)

    tasks = query.all()

    total = len(tasks)
    todo = len([t for t in tasks if t.status == "TODO"])
    progress = len([t for t in tasks if t.status == "IN_PROGRESS"])
    done = len([t for t in tasks if t.status == "DONE"])
    overdue = len([
        t for t in tasks
        if t.due_date and t.due_date < datetime.utcnow() and t.status != "DONE"
    ])

    tasks_per_user = {}
    for t in tasks:
        user_name = t.assigned_user.name if t.assigned_user else "Unassigned"
        tasks_per_user[user_name] = tasks_per_user.get(user_name, 0) + 1

    return {
        "total": total,
        "todo": todo,
        "in_progress": progress,
        "done": done,
        "overdue": overdue,
        "tasks_per_user": [
            {"user_name": name, "task_count": count}
            for name, count in tasks_per_user.items()
        ]
    }


@router.get("/projects")
def get_dashboard_projects(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == user.id
    ).all()

    projects = []
    for m in memberships:
        project = db.query(Project).filter(
            Project.id == m.project_id
        ).first()
        if project:
            projects.append({
                "id": project.id,
                "name": project.name
            })

    return projects