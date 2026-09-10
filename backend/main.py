from fastapi import FastAPI
from database.database import init_db
from database import models

app = FastAPI(
    title="CareerAI API",
    description="AI-Powered Career & Placement Assistant",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
def home():
    return {
        "message": "CareerAI Backend is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }