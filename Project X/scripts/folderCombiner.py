import os
import sys
import pandas as pd
import time


def main(folder):
    # For each file in the folder in the output folder, combine the data into a single DataFrame
    # and store in the output folder

    combined_data = []
    for file_name in os.listdir(f'output/{folder}'):
        df = pd.read_excel(f'output/{folder}/{file_name}')
        combined_data.append(df)
    
    combined_df = pd.concat(combined_data, ignore_index=True)

    combined_df.to_excel(f'output/{folder}_combined_xlsx_{time.strftime("%Y%m%d_%H%M%S")}.xlsx', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        folder = input("Folder name: ")
    elif len(sys.argv) == 2:
        folder = sys.argv[1]
    else:
        print("Usage: python jsonCombiner.py <folder>")
        sys.exit(1)

    main(folder)