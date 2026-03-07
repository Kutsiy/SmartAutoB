from fastapi import FastAPI
from router.auth import authRouter
from tools import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(authRouter)