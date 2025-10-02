from PyPDF2 import PdfReader

def parse_pdf(file_path, chunk_size=1000):
    """
    Parse PDF and split text into chunks
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    # Split into chunks
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks
