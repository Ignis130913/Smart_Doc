import fitz

def calculate_zoom_matrix(dpi: int) -> fitz.Matrix:
    """
    Calculate the zoom matrix based on DPI.
    
    Args:
        dpi (int): Desired DPI for the output images
    
    Returns:
        fitz.Matrix: Zoom matrix for rendering
    """
    zoom = dpi / 72 
    return fitz.Matrix(zoom, zoom)