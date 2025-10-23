import os
import time
import pdfSplitter
import documentExtractor_doctr as documentExtractor  # onze offline DocTR versie
import jsonCombiner
import folderCombiner

# Vraag gebruiker of het een map of enkel bestand is
folder_file = input("Folder or file? (folder/file): ").strip().lower()

if folder_file == "folder":
    folder = input("Enter the folder name: ").strip()
    # Haal lijst van bestanden op in de map
    files = [f for f in os.listdir(f'input/{folder}') if os.path.isfile(f'input/{folder}/{f}')]
else:
    folder = ""
    filename = input("Enter the filename: ").strip()
    files = [filename]

# Vraag gebruikersinput
limit = int(input("Enter the limit of pages to process: "))
split = input("Split files per page? (y/n): ").strip().lower()

# Loop door alle bestanden
for file in files:
    print(f"Processing file: {file}")
    # PDF splitsen of kopiëren
    pdfSplitter.main(input_filename=file, split=split, folder=folder)
    # OCR offline via DocTR
    documentExtractor.main(limit=limit, input_filename=file)
    # JSON-bestanden combineren
    jsonCombiner.main(filename=file, folder=folder)

# Als het een map is, combineer de output in één Excel
if folder != "":
    folderCombiner.main(folder)

print("All done! Offline workflow is compleet.")
