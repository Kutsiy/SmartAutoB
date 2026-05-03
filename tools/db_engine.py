from sqlmodel import create_engine, SQLModel, Session, select
from config import DATABASE_URL
import time
from sqlalchemy.exc import OperationalError
import models
from models import Roles



engine = create_engine(DATABASE_URL)

def wait_for_db():
    while True:
        try:
            with engine.connect():
                print("Database is ready!")
                break
        except OperationalError:
            print("Waiting for database...")
            time.sleep(1)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     existing_roles = session.exec(
    #         select(models.Role)
    #     ).all()
    #     existing_names = [role.name for role in existing_roles]
    #     roles_to_create = []
    #     if Roles.USER not in existing_names:
    #         roles_to_create.append(models.Role(name=Roles.USER))
    #     if Roles.ADMIN not in existing_names:
    #         roles_to_create.append(models.Role(name=Roles.ADMIN))
    #     if roles_to_create:
    #         session.add_all(roles_to_create)
    #         session.commit()