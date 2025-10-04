import docx
import PyPDF2
import logging

def parse_file(file):
    """Extracts text from a resume file."""
    logging.info(f"Parsing file: {file.filename}")
    if file.filename.endswith('.docx'):
        return _parse_docx(file)
    elif file.filename.endswith('.pdf'):
        return _parse_pdf(file)
    elif file.filename.endswith('.txt'):
        return _parse_txt(file)
    else:
        return None

def _parse_docx(file):
    """Extracts text from a .docx file."""
    try:
        doc = docx.Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception:
        return ""

def _parse_pdf(file):
    """Extracts text from a .pdf file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        return '\n'.join([page.extract_text() for page in pdf_reader.pages])
    except Exception:
        return ""

def _parse_txt(file):
    """Extracts text from a .txt file."""
    try:
        return file.read().decode('utf-8')
    except UnicodeDecodeError:
        file.seek(0)
        return file.read().decode('latin-1')
    except Exception:
        return ""