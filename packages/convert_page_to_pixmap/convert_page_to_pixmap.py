import fitz

def convert_page_to_pixmap(page: fitz.Page, matrix: fitz.Matrix) -> fitz.Pixmap:
    """
    Convert a PDF page to a PyMuPDF pixmap.
    
    Args:
        page (fitz.Page): PDF page to convert
        matrix (fitz.Matrix): Zoom matrix for rendering
    
    Returns:
        fitz.Pixmap: Rendered page as pixmap
    """
    return page.get_pixmap(matrix=matrix)