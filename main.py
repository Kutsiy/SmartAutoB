from fastapi import FastAPI
from router import auth_router, user_router, mail_router
from tools import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)
app.include_router(mail_router)
app.include_router(user_router)