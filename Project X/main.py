import sys
import os

# Zorg dat de scripts-map altijd gevonden wordt
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

# Importeer modules uit scripts
try:
    import pdfSplitter
    import documentExtractor
    import jsonCombiner
    import folderCombiner
except ModuleNotFoundError as e:
    print(f"Fout bij importeren: {e.name}")
    print("Controleer of de map 'scripts' in dezelfde map als main.py staat.")
    sys.exit(1)

# Vraag gebruiker om input
folder_or_file = input("Folder or file? (folder/file): ").strip().lower()

if folder_or_file == "file":
    filename = input("Enter the filename (with extension, e.g., document.pdf): ").strip()
    input_path = os.path.join(current_dir, "input", filename)
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f'File not found: {input_path}')

    limit = int(input("Enter the limit of pages to process: ").strip())
    split_choice = input("Split files per page? (y/n): ").strip().lower()
    split = split_choice == "y"

    # PDF splitsen
    if split:
        pdfSplitter.main(input_filename=filename, split=split, folder=current_dir)
    
    # Document extractor
    documentExtractor.main(limit=limit, input_filename=filename)

elif folder_or_file == "folder":
    folder_name = input("Enter the folder name: ").strip()
    folder_path = os.path.join(current_dir, folder_name)
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f'Folder not found: {folder_path}')

    # Combine JSONs in folder
    jsonCombiner.main(folder_path)

else:
    print("Ongeldige keuze, gebruik 'folder' of 'file'.")
