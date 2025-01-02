import fitz
import os

def open_pdf(pdf_path: str) -> fitz.Document:
    """
    Open a PDF file and return the document object.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        fitz.Document: Opened PDF document
    
    Raises:
        FileNotFoundError: If PDF file doesn't exist
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    return fitz.open(pdf_path)