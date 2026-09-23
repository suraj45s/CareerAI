from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
class ProfileUpdate(BaseModel):
    phone: str | None = None
    college: str | None = None
    degree: str | None = None
    branch: str | None = None
    graduation_year: int | None = None
    skills: str | None = None
    github: str | None = None
    linkedin: str | None = None