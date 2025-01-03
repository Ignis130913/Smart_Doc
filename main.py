import os
import json
import ast
import time
import pandas as pd

from image_extraction import image_extraction
from send_to_llm import send_to_llm

import warnings
warnings.filterwarnings("ignore")

pdf_path = 'data/pdf/'
images_path = 'data/output_images/'
output_dir = 'data/output/'
metadata_excel_path = 'metadata/metadata.xlsx'
batch_analysis_path = 'batchwise_analysis/batch_analysis.xlsx'

if not os.path.exists('batchwise_analysis'):
    os.makedirs('batchwise_analysis')

def save_metadata(func):
    def wrapper(*args, **kwargs):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        start_timestamp = time.time()
        pdf_file = args[0]
        
        try:
            status, reason = func(*args, **kwargs)
        except Exception as e:
            status, reason = "Failure", str(e)
        
        end_time = time.strftime("%Y-%m-%d %H:%M:%S")
        end_timestamp = time.time()
        process_time = end_timestamp - start_timestamp
        
        metadata_columns = ['filename', 'status', 'reason', 'start_time', 'end_time', 'process_time']
        
        if not os.path.exists(metadata_excel_path):
            metadata_df = pd.DataFrame(columns=metadata_columns)
        else:
            metadata_df = pd.read_excel(metadata_excel_path)
        
        metadata_df = pd.concat([metadata_df, pd.DataFrame([{
            'filename': pdf_file.replace('.pdf', ''),
            'status': status,
            'reason': reason,
            'start_time': start_time,
            'end_time': end_time,
            'process_time': process_time
        }])], ignore_index=True)
        
        metadata_df.to_excel(metadata_excel_path, index=False)
        return status, reason
    return wrapper

@save_metadata
def smart_doc(pdf_file):
    json_data = {}
    if pdf_file.endswith('.pdf'):
        result, reason = image_extraction(pdf_file)
    else:
        return "Failure", "Invalid File Format"

    if result == "Failure":
        return result, reason

    pdf_images_path = os.path.join(images_path, pdf_file.split('.')[0])

    for image_file in os.listdir(pdf_images_path):
        image_path = os.path.join(pdf_images_path, image_file)
        result, output = send_to_llm(image_path)

        time.sleep(10)

        if output == "Failure":
            return result, output

        if "429" in result:
            return "Failure", "LLM API Failed Due to Resource Limitation"

        try:
            json_data[image_file.split('.')[0]] = ast.literal_eval(output[8:-4])
        except:
            json_data[image_file.split('.')[0]] = {}

    with open(os.path.join(output_dir, pdf_file.split('.')[0] + '.json'), 'w') as f:
        json.dump(json_data, f)

    return "Success", "Data Processed Successfully"

def main():
    start_time = time.time()
    total_files = len(os.listdir(pdf_path))
    success_count = 0
    failure_count = 0

    for pdf_file in os.listdir(pdf_path):
        result, reason = smart_doc(pdf_file)
        if result == "Success":
            success_count += 1
        else:
            failure_count += 1

    end_time = time.time()
    total_time = end_time - start_time

    batch_data = {
        'batch_name': [f"Batch_{time.strftime('%Y%m%d_%H%M%S', time.localtime(start_time))}"],
        'total_files': [total_files],
        'success_count': [success_count],
        'failure_count': [failure_count],
        'total_time': [total_time]
    }

    if not os.path.exists(batch_analysis_path):
        batch_df = pd.DataFrame(columns=['batch_name', 'total_files', 'success_count', 'failure_count', 'total_time'])
        batch_df.to_excel(batch_analysis_path, index=False)

    batch_df = pd.read_excel(batch_analysis_path)
    batch_df = pd.concat([batch_df, pd.DataFrame(batch_data)], ignore_index=True)
    batch_df.to_excel(batch_analysis_path, index=False)

if __name__ == "__main__":
    main()