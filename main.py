from fastapi import FastAPI
from router.auth import authRouter
from router.mail import mailRouter
from tools import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(authRouter)
app.include_router(mailRouter)