import pdfplumber

def extract_pdf_text(path):
    """
    Extracts plain text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text
