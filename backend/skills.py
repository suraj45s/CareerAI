SKILLS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "React",
    "Node.js",
    "SQL",
    "MongoDB",
    "DSA",
    "HTML",
    "CSS",
    "Git",
    "GitHub",
    "FastAPI",
    "Docker"
]
def extract_skills(resume_text: str):
    found_skills = []

    resume_text_lower = resume_text.lower()

    for skill in SKILLS:
        if skill.lower() in resume_text_lower:
            found_skills.append(skill)

    return found_skills