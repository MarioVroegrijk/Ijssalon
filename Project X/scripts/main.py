import os
import time
import pdfSplitter
import documentExtractor_doctr as documentExtractor
import jsonCombiner
import folderCombiner

def ensure_folder_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# Controleer basisfolders
for folder in ['input', 'temp/files_split', 'temp/json_export', 'output']:
    ensure_folder_exists(folder)

folder_file = input("Folder or file? (folder/file): ").strip().lower()

if folder_file == "folder":
    folder = input("Enter the folder name: ").strip()
    files = [f for f in os.listdir(f'input/{folder}') if os.path.isfile(f'input/{folder}/{f}')]
else:
    folder = ""
    filename = input("Enter the filename: ").strip()
    files = [filename]

limit = int(input("Enter the limit of pages to process: "))
split = input("Split files per page? (y/n): ").strip().lower()

for file in files:
    print(f"Processing file: {file}")
    pdfSplitter.main(input_filename=file, split=split, folder=folder)
    documentExtractor.main(limit=limit, input_filename=file)
    jsonCombiner.main(filename=file, folder=folder)

if folder != "":
    folderCombiner.main(folder)

print("All done!")
