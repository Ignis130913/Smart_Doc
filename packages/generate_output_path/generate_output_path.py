import os

def generate_output_path(output_dir: str, page_number: int, format: str = 'png') -> str:
    """
    Generate the output path for a page image.
    
    Args:
        output_dir (str): Output directory path
        page_number (int): Page number
        format (str): Image format extension
    
    Returns:
        str: Complete output path
    """
    return os.path.join(output_dir, f'page_{page_number + 1}.{format.lower()}')