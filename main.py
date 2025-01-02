import os
import json
import ast
import time

from image_extraction import image_extraction
from send_to_llm import send_to_llm

import warnings
warnings.filterwarnings("ignore")

pdf_path = 'data/pdf/'
images_path = 'data/output_images/'
output_dir = 'data/output/'

def main():
    for pdf_file in os.listdir(pdf_path):
        
        json_data = {}
        print(f"Processing {pdf_file}")
        
        if pdf_file.endswith('.pdf'):
            result, reason = image_extraction(pdf_file)
            
        if result == "Failure":
            print(f"Error: {reason}")
            continue
            
        pdf_images_path = os.path.join(images_path, pdf_file.split('.')[0])
        
        for image_file in os.listdir(pdf_images_path):
            print(f"Processing {image_file}")
            
            image_path = os.path.join(pdf_images_path, image_file)
            result, output = send_to_llm(image_path)
            
            time.sleep(10)
            
            if output == "Failure":
                print(f"Error: {result}")
                continue
            
            if "429" in result or ("{" not in result and "}" not in result): result = {}
            
            try:
                json_data[image_file.split('.')[0]] = ast.literal_eval(output[8 : -4])
            
            except:
                json_data[image_file.split('.')[0]] = {}
            
            print(f"Processing {image_file} completed")
            
        with open(os.path.join(output_dir, pdf_file.split('.')[0] + '.json'), 'w') as f:
            json.dump(json_data, f)
            
        print(f"Processing {pdf_file} completed")
    
    print("All files processed")

if __name__ == "__main__":
    main()