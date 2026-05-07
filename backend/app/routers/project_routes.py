from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Project, ProjectMember, User
from schemas import ProjectSchema, AddMemberSchema
from dependencies import get_current_user

router = APIRouter(prefix="/projects")


def _is_admin(db: Session, user: User, project_id: int):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id,
        ProjectMember.role == "Admin"
    ).first()


def _is_member(db: Session, user: User, project_id: int):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()


@router.post("/")
def create_project(
    data: ProjectSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    project = Project(
        name=data.name,
        created_by=user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    member = ProjectMember(
        project_id=project.id,
        user_id=user.id,
        role="Admin"
    )

    db.add(member)
    db.commit()

    return project


@router.get("/")
def get_projects(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == user.id
    ).all()

    project_ids = [m.project_id for m in memberships]
    projects = db.query(Project).filter(
        Project.id.in_(project_ids)
    ).all()

    return projects


@router.get("/{project_id}/members")
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = _is_member(db, current_user, project_id)
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this project")

    members = db.query(ProjectMember).options(joinedload(ProjectMember.user)).filter(
        ProjectMember.project_id == project_id
    ).all()

    return [
        {
            "id": m.user.id,
            "name": m.user.name,
            "email": m.user.email,
            "role": m.role,
            "is_current_user": m.user_id == current_user.id
        }
        for m in members
    ]


@router.post("/{project_id}/members")
@router.post("/{project_id}/add-member/{user_id}")
def add_member(
    project_id: int,
    data: AddMemberSchema = None,
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_id is None:
        user_id = data.user_id

    if not _is_admin(db, current_user, project_id):
        raise HTTPException(status_code=403, detail="Only admin allowed")

    if db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first():
        raise HTTPException(status_code=400, detail="User already a member")

    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role="Member"
    )

    db.add(member)
    db.commit()

    return {"message": "Member added"}


@router.delete("/{project_id}/remove-member/{user_id}")
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not _is_admin(db, current_user, project_id):
        raise HTTPException(status_code=403, detail="Only admin allowed")

    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(status_code=404, detail="Project member not found")

    db.delete(membership)
    db.commit()

    return {"message": "Member removed"}


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).all()
    return [{"id": user.id, "name": user.name, "email": user.email} for user in users]