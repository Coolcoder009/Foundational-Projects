import re

def get_email(text):
    mail = re.search(r'[\w\,\-]+@[\w\.\-]+', text)
    return mail.group(0) if mail else "NA"

def get_number(text):
    number = re.search(r'(?:\+91[\-\s]?|91[\-\s]?)?[6-9]\d{9}\b',text)
    return number.group(0) if number else "NA"

def get_sections(text):
    mandatory_sections = ["skills", "achievements", "experience", "education", "projects"]
    return [section for section in mandatory_sections if section.lower() in text.lower() ]

def get_skills(text):
    mandatory_skills = ["python", "sql", "tensorflow", "pytorch", "docker", "fastapi", "deep learning", "machine learning"]
    return [skill for skill in mandatory_skills if skill.lower() in text.lower()]

def extract_section_content(text):
    sections = ["skills", "achievements", "experience", "education", "projects", "reference"]
    section_pattern = "|".join([fr"\b{sec}\b" for sec in sections])
    # \bskills\b|\bachievements\b|\bexperience\b|\beducation\b|\bprojects\b

    pattern = re.compile(fr"(?P<heading>{section_pattern})\s*[:\-]?\s*", re.IGNORECASE)
    # Find all headings with their positions
    matches = list(pattern.finditer(text))
    extracted = {}

    for i, match in enumerate(matches):
        section = match.group("heading").lower()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        extracted[section] = content

    return extracted
