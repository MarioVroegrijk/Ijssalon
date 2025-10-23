import os
import pandas as pd
import time

def ensure_folder_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def main(folder):
    """
    Combine all Excel files in output/{folder} into one Excel file.
    """

    input_folder = os.path.join('output', folder)
    if not os.path.exists(input_folder):
        print(f"No such folder: {input_folder}")
        return

    combined_data = []
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(input_folder, file_name))
            combined_data.append(df)

    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        output_folder = os.path.join('output')
        ensure_folder_exists(output_folder)
        output_file = os.path.join(
            output_folder, f'{folder}_combined_{time.strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
        combined_df.to_excel(output_file, index=False)
        print(f"Combined file saved as: {output_file}")
    else:
        print(f"No Excel files found in {input_folder} to combine.")

if __name__ == "__main__":
    folder = input("Folder name to combine: ").strip()
    main(folder)
