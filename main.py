from fastapi import FastAPI
from router.auth import authRouter

app = FastAPI()

app.include_router(authRouter)