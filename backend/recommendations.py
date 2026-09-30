def calculate_match(user_skills, required_skills):
    if not required_skills:
        return 0

    user_skills = {
        skill.strip().lower()
        for skill in user_skills.split(",")
    }

    required_skills = {
        skill.strip().lower()
        for skill in required_skills.split(",")
    }

    matched_skills = user_skills.intersection(required_skills)
    print("USER SKILLS:", user_skills)
    print("REQUIRED SKILLS:", required_skills)
    print("MATCHED:", matched_skills)

    match_percentage = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return round(match_percentage)