from tools import SessionDep
from models import Role, UserRole
from sqlmodel import select
from fastapi import HTTPException, status

def find_and_add_role(user_id, session: SessionDep):
    role: Role = session.exec(select(Role).where(Role.name == "USER")).first()
    if not role:
        raise HTTPException(detail="Role not found", status_code=status.HTTP_404_NOT_FOUND)
    
    userRole = UserRole(user_id=user_id, role_id=role.id)
    session.add(userRole)
    session.commit()

    return role
