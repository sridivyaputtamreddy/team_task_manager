from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Task, ProjectMember, User
from schemas import TaskSchema, UpdateTaskSchema, AssignTaskSchema
from dependencies import get_current_user

router = APIRouter(prefix="/tasks")


def _is_project_admin(db: Session, user: User, project_id: int):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id,
        ProjectMember.role == "Admin"
    ).first()


def _is_project_member(db: Session, user: User, project_id: int):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()


@router.post("/")
def create_task(
    data: TaskSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not _is_project_admin(db, user, data.project_id):
        raise HTTPException(status_code=403, detail="Only admin can create tasks")

    task = Task(
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        priority=data.priority,
        assigned_to=data.assigned_to,
        project_id=data.project_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/")
def get_tasks(
    project_id: int = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Task).options(joinedload(Task.assigned_user))

    if project_id:
        membership = _is_project_member(db, user, project_id)
        if not membership:
            raise HTTPException(status_code=403, detail="Not a member of this project")

        if membership.role == "Admin":
            query = query.filter(Task.project_id == project_id)
        else:
            query = query.filter(
                Task.project_id == project_id,
                Task.assigned_to == user.id
            )
    else:
        query = query.filter(Task.assigned_to == user.id)

    tasks = query.all()
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "status": task.status,
            "project_id": task.project_id,
            "assigned_to": task.assigned_to,
            "assigned_user_name": task.assigned_user.name if task.assigned_user else None,
            "created_at": task.created_at.isoformat() if task.created_at else None
        }
        for task in tasks
    ]


@router.put("/{task_id}")
def update_task(
    task_id: int,
    data: UpdateTaskSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    is_admin = _is_project_admin(db, user, task.project_id)
    if task.assigned_to != user.id and not is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    task.status = data.status
    db.commit()

    return {"message": "Task updated"}


@router.put("/{task_id}/assign")
def assign_task(
    task_id: int,
    data: AssignTaskSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if not _is_project_admin(db, user, task.project_id):
        raise HTTPException(status_code=403, detail="Only admin can assign tasks")

    if data.assigned_to:
        member = db.query(ProjectMember).filter(
            ProjectMember.project_id == task.project_id,
            ProjectMember.user_id == data.assigned_to
        ).first()
        if not member:
            raise HTTPException(status_code=400, detail="User is not a member of this project")

    task.assigned_to = data.assigned_to
    db.commit()

    return {"message": "Task assigned successfully"}