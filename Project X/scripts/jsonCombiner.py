import os
import sys
import json
import pandas as pd

def extract_value(field):
    """Extract the 'value' from the field dictionary if it exists."""
    if isinstance(field, dict) and 'value' in field:
        return field['value']
    return field

def extract_fields_from_json(json_folder):
    """Combine all JSON files in a folder into a DataFrame."""
    combined_data = []

    for file_name in os.listdir(json_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(json_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                for page in data:  # Elke pagina in de JSON
                    for line in page.get("lines", []):
                        combined_data.append({
                            "page": page.get("page"),
                            "text": line.get("text"),
                            "confidence": line.get("confidence")
                        })

    df = pd.DataFrame(combined_data)

    # Verwijder eventuele dict-waardes die nog in de DataFrame zitten
    for column in df.columns:
        df[column] = df[column].apply(lambda x: extract_value(x) if isinstance(x, dict) else x)

    return df

def save_to_excel(dataframe, output_path):
    """Save the combined DataFrame to an Excel file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dataframe.to_excel(output_path, index=False)

def main(filename, folder=""):
    json_folder = os.path.join('temp/json_export', filename)
    if folder:
        output_path = os.path.join('output', folder, f"{filename}_combined.xlsx")
    else:
        output_path = os.path.join('output', f"{filename}_combined.xlsx")

    df = extract_fields_from_json(json_folder)
    save_to_excel(df, output_path)
    print(f"Saved combined Excel to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        folder_name = sys.argv[1]
        main(filename=folder_name)
    elif len(sys.argv) == 3:
        main(filename=sys.argv[1], folder=sys.argv[2])
    else:
        filename = input("Enter the filename to combine: ")
        folder = input("Enter folder (optional): ")
        main(filename, folder)
