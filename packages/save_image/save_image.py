from PIL import Image

def save_image(image: Image.Image, output_path: str, format: str = 'PNG') -> None:
    """
    Save a PIL Image to file.
    
    Args:
        image (Image.Image): PIL Image to save
        output_path (str): Path where the image will be saved
        format (str): Image format (default: 'PNG')
    """
    image.save(output_path, format)
    print(f'Saved image to: {output_path}')