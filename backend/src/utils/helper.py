# Placeholder helper functions

def allowed_file(filename):
    """
    Checks if the uploaded file is a PDF.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}
