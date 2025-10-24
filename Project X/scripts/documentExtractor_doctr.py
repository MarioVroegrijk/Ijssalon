import os
from doctr.models import ocr_predictor, db_resnet50, crnn_vgg16_bn
from pdf2image import convert_from_path
import json

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
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{file_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=default_converter)

def main(limit, input_filename):
    # Paden naar lokale modellen
    det_model_path = os.path.join("models", "fast_base-688a8b34.pt")
    reco_model_path = os.path.join("models", "vitstr_small.pt")  # voeg toe als apart bestand

    # Laad detectiemodel volledig offline
    det_model = db_resnet50(pretrained=False)
    det_model.from_pretrained(det_model_path, map_location="cpu")

    # Laad herkenningsmodel volledig offline
    reco_model = crnn_vgg16_bn(pretrained=False)
    reco_model.from_pretrained(reco_model_path, map_location="cpu")

    # Predictor volledig offline
    predictor = ocr_predictor(det_arch=det_model, reco_arch=reco_model, pretrained=False)

    folder_path = os.path.join('temp/files_split', input_filename)
    os.makedirs(os.path.join('temp/json_export', input_filename), exist_ok=True)

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
