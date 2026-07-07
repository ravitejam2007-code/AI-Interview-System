def check_ats(resume_text, job_skills=None):
    """
    Computes ATS compatibility score, matched/missing skills and formatting metrics.
    """
    if not job_skills:
        # Default target job skills if none provided
        job_skills = ["python", "machine learning", "flask", "sql", "react", "javascript"]
        
    matched = []
    missing = []
    
    for skill in job_skills:
        if skill.lower() in resume_text.lower():
            matched.append(skill)
        else:
            missing.append(skill)
            
    # Calculate skill match base score (out of 80)
    skill_match_percentage = len(matched) / len(job_skills) if job_skills else 0
    base_score = int(skill_match_percentage * 80)
    
    # Formatting analysis (out of 20)
    formatting_score = 20
    reasons = []
    
    if len(resume_text) < 200:
        formatting_score -= 10
        reasons.append("Resume content is too short. Add more professional details.")
    elif len(resume_text) > 12000:
        formatting_score -= 5
        reasons.append("Resume content is extremely long. Keep it under 2 pages.")
        
    if not re_has_structure(resume_text):
        formatting_score -= 5
        reasons.append("Missing standard sections like Education, Experience or Skills.")
        
    ats_score = base_score + formatting_score
    ats_score = min(max(ats_score, 0), 100)
    
    return {
        "ats_score": ats_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "formatting_score": formatting_score,
        "suggestions": reasons
    }

def re_has_structure(text):
    """
    Checks if common resume section headers are present in the text.
    """
    headers = ["experience", "education", "skills", "projects", "summary", "employment"]
    text_lower = text.lower()
    matches = sum(1 for header in headers if header in text_lower)
    return matches >= 2
