from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import init_db, AsyncSessionLocal
from database import models
from database.models import User, StudentProfile, Resume, Job
from database.schemas import UserCreate, ProfileUpdate
from security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from security import SECRET_KEY, ALGORITHM
security = HTTPBearer()
from fastapi.responses import FileResponse
from pypdf import PdfReader
from skills import extract_skills
from recommendations import calculate_match

app = FastAPI(
    title="CareerAI API",
    description="AI-Powered Career & Placement Assistant",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@app.post("/register")
async def register(user: UserCreate):
    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(User).where(User.email == user.email)
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        new_user = User(
    name=user.name,
    email=user.email,
    password=hash_password(user.password)
)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id
        }
@app.post("/login")
async def login(email: str, password: str):
    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(User).where(User.email == email)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(user.id)

        return {
    "message": "Login successful",
    "access_token": access_token,
    "token_type": "bearer",
    "user_id": user.id,
    "name": user.name
}
@app.get("/profile")
async def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    async with AsyncSessionLocal() as db:
        result = await db.execute(
    select(User, StudentProfile)
    .outerjoin(
        StudentProfile,
        User.id == StudentProfile.user_id
    )
    .where(User.id == user_id)
)

        row = result.first()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        user, profile = row


        return {
    "id": user.id,
    "name": user.name,
    "email": user.email,
    "phone": profile.phone if profile else None,
    "college": profile.college if profile else None,
    "degree": profile.degree if profile else None,
    "branch": profile.branch if profile else None,
    "graduation_year": profile.graduation_year if profile else None,
    "skills": profile.skills if profile else None,
    "github": profile.github if profile else None,
    "linkedin": profile.linkedin if profile else None
}

    
@app.put("/profile")
async def update_profile(
    profile: ProfileUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(StudentProfile).where(
                StudentProfile.user_id == user_id
            )
        )

        existing_profile = result.scalar_one_or_none()

        if existing_profile:
            existing_profile.phone = profile.phone
            existing_profile.college = profile.college
            existing_profile.degree = profile.degree
            existing_profile.branch = profile.branch
            existing_profile.graduation_year = profile.graduation_year
            existing_profile.skills = profile.skills
            existing_profile.github = profile.github
            existing_profile.linkedin = profile.linkedin

        else:
            existing_profile = StudentProfile(
                user_id=user_id,
                phone=profile.phone,
                college=profile.college,
                degree=profile.degree,
                branch=profile.branch,
                graduation_year=profile.graduation_year,
                skills=profile.skills,
                github=profile.github,
                linkedin=profile.linkedin
            )

            db.add(existing_profile)

        await db.commit()
        await db.refresh(existing_profile)

        return {
            "message": "Profile updated successfully",
            "profile_id": existing_profile.id
        } 
    
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    reader = PdfReader(file_path)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
          resume_text += text + "\n"
    extracted_skills = extract_skills(resume_text)

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Resume).where(
                Resume.user_id == user_id
            )
        )

        existing_resume = result.scalar_one_or_none()

        if existing_resume:
           existing_resume.file_name = file.filename
           existing_resume.file_path = file_path
           existing_resume.resume_text = resume_text
           existing_resume.extracted_skills = ", ".join(extracted_skills)

        else:
            new_resume = Resume(
                user_id=user_id,
                file_name=file.filename,
                file_path=file_path,
                resume_text=resume_text,
                extracted_skills=", ".join(extracted_skills)
                
            )

            db.add(new_resume)

        await db.commit()

    return {
        "message": "Resume uploaded successfully",
        "user_id": user_id,
        "file_name": file.filename,
        "file_path": file_path
    }
@app.get("/resume")
async def get_resume(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Resume).where(
                Resume.user_id == user_id
            )
        )

        resume = result.scalar_one_or_none()

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found"
            )

        return {
    "id": resume.id,
    "file_name": resume.file_name,
    "file_path": resume.file_path,
    "extracted_skills": resume.extracted_skills
}
@app.get("/resume/view")
async def view_resume(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Resume).where(
                Resume.user_id == user_id
            )
        )

        resume = result.scalar_one_or_none()

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found"
            )

        if not os.path.exists(resume.file_path):
            raise HTTPException(
                status_code=404,
                detail="Resume file not found"
            )

        return FileResponse(
            resume.file_path,
            media_type="application/pdf",
            filename=resume.file_name
        )
@app.post("/jobs")
async def create_job(
    title: str,
    company: str,
    location: str = "",
    description: str = "",
    required_skills: str = "",
    apply_url: str = ""
):
    async with AsyncSessionLocal() as db:

        new_job = Job(
            title=title,
            company=company,
            location=location,
            description=description,
            required_skills=required_skills,
            apply_url=apply_url
        )

        db.add(new_job)
        await db.commit()
        await db.refresh(new_job)

        return {
            "message": "Job created successfully",
            "job_id": new_job.id
        }
@app.get("/jobs")
async def get_jobs():
    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Job)
        )

        jobs = result.scalars().all()

        return [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "required_skills": job.required_skills,
                "apply_url": job.apply_url
            }
            for job in jobs
        ]
@app.get("/recommended-jobs")
async def recommended_jobs(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    async with AsyncSessionLocal() as db:

        # Get user's resume
        result = await db.execute(
            select(Resume).where(Resume.user_id == user_id)
        )

        resume = result.scalar_one_or_none()

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found"
            )

        user_skills = resume.extracted_skills or ""

        # Get all jobs
        result = await db.execute(select(Job))
        jobs = result.scalars().all()

        recommendations = []

        for job in jobs:

         match_percentage = calculate_match(
         user_skills,
         job.required_skills or ""
    )
         print(
    "JOB:",
    job.title,
    "| REQUIRED:",
    job.required_skills,
    "| MATCH:",
    match_percentage
)

         if match_percentage >= 30:

          recommendations.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "required_skills": job.required_skills,
            "apply_url": job.apply_url,
            "match_percentage": match_percentage
        })

        # Highest match first
        recommendations.sort(
            key=lambda x: x["match_percentage"],
            reverse=True
        )

        return recommendations