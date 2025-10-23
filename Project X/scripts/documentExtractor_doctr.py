import os
import sys
import json
from doctr.models import ocr_predictor
from pdf2image import convert_from_path

def ensure_folder_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def default_converter(o):
    from datetime import date
    if isinstance(o, date):
        return o.isoformat()

def process_pdf(file_path, predictor):
    pages = convert_from_path(file_path)
    results = []

    for page_number, page_image in enumerate(pages, start=1):
        result = predictor([page_image])
        page_data = []

        for block in result[0].blocks:
            for line in block.lines:
                line_text = " ".join([el.value for el in line.elements])
                line_conf = sum([el.confidence for el in line.elements]) / len(line.elements)
                page_data.append({"text": line_text, "confidence": line_conf})

        results.append({"page": page_number, "lines": page_data})

    return results

def save_extracted_data(file_name, data, input_filename):
    output_folder = os.path.join('temp/json_export', input_filename)
    ensure_folder_exists(output_folder)
    output_path = os.path.join(output_folder, f"{file_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=default_converter)

def main(limit, input_filename):
    predictor = ocr_predictor(pretrained=True)
    folder_path = os.path.join('temp/files_split', input_filename)

    ensure_folder_exists(os.path.join('temp/json_export', input_filename))

    processed_pages = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf") and processed_pages < limit:
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing {file_path}")

            try:
                extracted_data = process_pdf(file_path, predictor)
                save_extracted_data(os.path.splitext(file_name)[0], extracted_data, input_filename)
                print(f"Saved JSON for {file_name}")
                processed_pages += 1
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        limit = int(sys.argv[1])
        input_filename = sys.argv[2]
    else:
        input_filename = input("Enter the filename: ")
        limit = int(input("Enter the limit of pages to process: "))

    main(limit=limit, input_filename=input_filename)
