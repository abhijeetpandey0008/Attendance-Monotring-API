from fastapi import FastAPI

from src.database.database import Base, engine
from src.api.routes import auth, batch, session, attendance , monitoring ,programme
from src.models import user

app = FastAPI(title="Attendance Management API")

# Create tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(auth.router)
app.include_router(batch.router)
app.include_router(session.router)
app.include_router(attendance.router)
app.include_router(monitoring.router)
app.include_router(programme.router)

# Root endpoint (clean + professional)
@app.get("/")
def root():
    return {"message": "Attendance Management API is running 🚀"}