import os

def create_output_directory(output_dir: str) -> None:
    """
    Create the output directory if it doesn't exist.
    
    Args:
        output_dir (str): Path to the output directory
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")