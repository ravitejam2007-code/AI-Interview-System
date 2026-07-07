import re

def clean_text(text):
    """
    Cleans raw text by removing excessive whitespaces, newlines and special characters.
    """
    if not text:
        return ""
    # Replace multiple spaces/newlines with single space
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()
