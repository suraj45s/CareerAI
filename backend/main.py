from fastapi import FastAPI

app = FastAPI(
    title="CareerAI API",
    description="AI-Powered Career & Placement Assistant",
    version="1.0.0"
)


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