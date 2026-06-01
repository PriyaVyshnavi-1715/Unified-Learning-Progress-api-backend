from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import close_db_connection, db
from app.routes import assignments, auth, coding_stats, dashboard, lms_progress, skills, students

settings = get_settings()

app = FastAPI(
    title="Unified Learning Progress API",
    description="A FastAPI service for LMS progress, coding stats, skills, assignments, and completion dashboards.",
    version="1.0.0",
)

origins = ["*"] if settings.cors_origins == "*" else [origin.strip() for origin in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(skills.router)
app.include_router(lms_progress.router)
app.include_router(coding_stats.router)
app.include_router(assignments.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def startup() -> None:
    await db.users.create_index("email", unique=True)


@app.on_event("shutdown")
async def shutdown() -> None:
    await close_db_connection()


@app.get("/")
async def root():
    return {"message": "Unified Learning Progress API is running", "docs": "/docs"}
