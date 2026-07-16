from fastapi import FastAPI

from app.routers import auth, students, admissions, dashboard
from app.database.init_db import init_db


app = FastAPI(
    title="LSMS API",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(students.router)
app.include_router(admissions.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {
        "message": "Welcome to LSMS API"
    }