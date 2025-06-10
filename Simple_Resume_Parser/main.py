import os
from fastapi import FastAPI, UploadFile, File
from file import parse_pdf, parse_docs
from get_data import get_email, get_number, get_sections, get_skills, extract_section_content

app = FastAPI()

@app.post("/parse_resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        text = parse_pdf(file.file)
    elif file.filename.endswith(".docx"):
        text = parse_docs(file.file)
    else:
        return {"Only pdfs and docs are allowed!"}
    email = get_email(text)
    number = get_number(text)
    sections = get_sections(text)
    skills = get_skills(text)
    content = extract_section_content(text)
    return{
            "Email": email,
            "Mobile-Number": number,
            "Sections": sections,
            "Skills": skills,
            "Education": content["education"],
            "Experience": content["experience"],
            "Projects": content["projects"],
            "Achievements": content["achievements"],
            "References": content["reference"]
        }

