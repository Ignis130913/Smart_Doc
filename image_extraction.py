import fitz 
from PIL import Image
import io
import os
from typing import List, Tuple

from packages.calculate_zoom_matrix.calculate_zoom_matrix import calculate_zoom_matrix
from packages.create_output_dir.create_output_dir import create_output_directory
from packages.convert_page_to_pixmap.convert_page_to_pixmap import convert_page_to_pixmap
from packages.generate_output_path.generate_output_path import generate_output_path
from packages.open_pdf.open_pdf import open_pdf
from packages.pixmap_to_pil_image.pixmap_to_pil_image import pixmap_to_pil_image
from packages.save_image.save_image import save_image

pdf_dir = "data/pdf/"
output_dir = "data/output_images"

def process_single_page(page: fitz.Page, matrix: fitz.Matrix, output_path: str) -> str:
    """
    Process a single PDF page and convert it to an image.
    
    Args:
        page (fitz.Page): PDF page to process
        matrix (fitz.Matrix): Zoom matrix for rendering
        output_path (str): Path to save the output image
    
    Returns:
        str: Path to the saved image
    """
    pixmap = convert_page_to_pixmap(page, matrix)
    image = pixmap_to_pil_image(pixmap)
    save_image(image, output_path)
    return output_path

def convert_pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 300) -> List[str]:
    """
    Main function to convert PDF pages to images.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save the images
        dpi (int): Resolution for the output images (default: 300)
    
    Returns:
        List[str]: List of paths to the generated images
    """
    try:
        create_output_directory(output_dir)
        pdf_document = open_pdf(pdf_path)
        matrix = calculate_zoom_matrix(dpi)
        image_paths = []
        
        for page_number in range(pdf_document.page_count):
            output_path = generate_output_path(output_dir, page_number)
            page = pdf_document[page_number]
            image_path = process_single_page(page, matrix, output_path)
            image_paths.append(image_path)
            
        pdf_document.close()
        
        return image_paths
    
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        raise

def image_extraction(pdf_file: str) -> Tuple[str, str]:
    """
    Main entry point of the script.
    """
        
    pdf_path = os.path.join(pdf_dir, pdf_file)
    output_path = os.path.join(output_dir, pdf_file.split(".")[0])
    
    try:
        image_paths = convert_pdf_to_images(pdf_path, output_path)
        print(f"\nSuccessfully converted PDF to {len(image_paths)} images")
        print("Output images:")
        for path in image_paths:
            print(f"- {path}")
    except Exception as e:
        return "Failure", f"An error occurred: {str(e)}"

    return "Success", "All PDFs converted successfully"

# Testing
if __name__ == "__main__":
    image_extraction()