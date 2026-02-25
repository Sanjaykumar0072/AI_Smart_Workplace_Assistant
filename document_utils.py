import PyPDF2

def read_pdf(file):
    """
    Reads uploaded PDF file and returns extracted text.
    """
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text