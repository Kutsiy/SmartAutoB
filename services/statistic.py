from models import User
from tools import SessionDep
from sqlmodel import select

def get_count_of_users(session: SessionDep):
    return len(session.exec(select(User.id)).all())


