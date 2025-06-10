from pypdf import PdfReader
import docx

def parse_pdf(resume_path):
    reader = PdfReader(resume_path)
    page = reader.pages[0]
    text = page.extract_text()
    return text

def parse_docs(resume_path):
    doc = docx.Document(resume_path)
    return "\n".join([para.text for para in doc.paragraphs])