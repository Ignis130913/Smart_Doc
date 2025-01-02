from PIL import Image
import fitz

def pixmap_to_pil_image(pixmap: fitz.Pixmap) -> Image.Image:
    """
    Convert a PyMuPDF pixmap to a PIL Image.
    
    Args:
        pixmap (fitz.Pixmap): PyMuPDF pixmap to convert
    
    Returns:
        Image.Image: PIL Image object
    """
    return Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)