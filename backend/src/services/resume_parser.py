import re
from src.utils.pdf_reader import extract_pdf_text

def extract_text_from_pdf(path):
    """
    Extracts text from pdf.
    """
    return extract_pdf_text(path)

def extract_skills(text):
    """
    Extracts known skills from the resume text.
    """
    required_skills = [
        "python", "machine learning", "flask", "sql", "react", "javascript",
        "aws", "docker", "django", "nodejs", "git", "java", "c++", "html", "css"
    ]
    matched_skills = []
    for skill in required_skills:
        # Use word boundary check to avoid substring issues (e.g. 'git' matching inside 'digital')
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text.lower()):
            matched_skills.append(skill)
    return matched_skills

def extract_education(text):
    """
    Extracts education details using standard keyword lookups.
    """
    education_keywords = ["bachelor", "master", "phd", "degree", "b.tech", "m.tech", "b.sc", "m.sc", "university", "college"]
    education = []
    for line in text.split('\n'):
        if any(keyword in line.lower() for keyword in education_keywords):
            education.append(line.strip())
    # Return unique education lines up to 3
    return list(set(education))[:3]

def extract_experience(text):
    """
    Extracts work experience highlights.
    """
    experience_keywords = ["experience", "worked as", "developer", "engineer", "intern", "years of experience"]
    experience = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in experience_keywords):
            # Grab current and next line for context
            ctx = line.strip()
            if i + 1 < len(lines):
                ctx += " " + lines[i+1].strip()
            experience.append(ctx)
    return list(set(experience))[:3]

def parse_resume(file_path):
    """
    Parses resume PDF to return structured data.
    """
    text = extract_text_from_pdf(file_path)
    return {
        "text": text,
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
