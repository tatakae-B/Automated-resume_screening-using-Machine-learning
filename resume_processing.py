import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF using PyPDF2.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        if not text.strip():
            print(f"Warning: No text extracted from {pdf_path}.")
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def preprocess_text(text):
    """
    Preprocesses text for comparison:
    - Converts to lowercase.
    - Retains alphanumeric characters and essential symbols.
    - Normalizes whitespace.
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)  # Keep essential symbols like '.' and ','
    text = ' '.join(text.split())  # Normalize spaces
    return text
