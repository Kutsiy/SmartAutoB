from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from router import auth_router, user_router, mail_router, work_type_router, service_router, category_router, appointment_router, statistic_router
from tools import create_db_and_tables
from pathlib import Path

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:3001"]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()\
    
app.add_middleware(CORSMiddleware,  allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(RequestValidationError)
async def handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Bad request"}
    )

app.include_router(auth_router)
app.include_router(mail_router)
app.include_router(user_router)
app.include_router(work_type_router)
app.include_router(service_router)
app.include_router(category_router)
app.include_router(appointment_router)
app.include_router(statistic_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
