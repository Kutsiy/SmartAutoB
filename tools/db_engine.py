from sqlmodel import create_engine, SQLModel, Session
from config import DATABASE_URL
import time
from sqlalchemy.exc import OperationalError
import models 



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
    user_role = models.Role(name="USER")
    admin_role = models.Role(name="ADMIN")
    session = Session(engine)
    session.add(user_role)
    session.add(admin_role)
    session.commit()
    session.close()