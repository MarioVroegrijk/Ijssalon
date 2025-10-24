import sys
import os

# Voeg scripts-map toe aan sys.path zodat imports werken
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
sys.path.append(scripts_dir)

try:
    import pdfSplitter
    import documentExtractor
    import jsonCombiner
    import folderCombiner
except ModuleNotFoundError as e:
    print(f"Fout bij importeren: {e.name}")
    sys.exit(1)

def main():
    input_folder = os.path.join(current_dir, "input")
    output_folder = os.path.join(current_dir, "output")
    os.makedirs(output_folder, exist_ok=True)

    # Vind PDF-bestanden automatisch
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("Geen PDF-bestanden gevonden in de map 'input'.")
        return

    # Als er maar één bestand is, kies die automatisch
    if len(pdf_files) == 1:
        file_to_process = pdf_files[0]
        print(f"Één PDF gevonden, automatisch geselecteerd: {file_to_process}")
    else:
        print("Meerdere PDF-bestanden gevonden:")
        for idx, f in enumerate(pdf_files):
            print(f"{idx+1}: {f}")
        choice = int(input("Kies het bestandnummer om te verwerken: "))
        file_to_process = pdf_files[choice - 1]

    input_path = os.path.join(input_folder, file_to_process)

    # Vraag aantal pagina's (standaard 100)
    limit = input("Enter the limit of pages to process (default 100): ")
    limit = int(limit) if limit.strip() else 100

    # Vraag of splitsen
    split_choice = input("Split files per page? (y/n, default y): ").strip().lower()
    split = split_choice != "n"

    # Splits PDF indien gevraagd
    if split:
        print("Splitsen van PDF per pagina...")
        pdfSplitter.main(input_filename=input_path, split=True, folder=output_folder)
    else:
        output_folder = input_folder  # geen split

    # Verwerk OCR / documentextractie
    print("Start documentextractie...")
    documentExtractor.main(limit=limit, input_filename=input_path, output_folder=output_folder)

    # Combineer JSON-bestanden (optioneel)
    print("Combineer JSON-bestanden...")
    jsonCombiner.main(folder=output_folder)

    # Combineer resultaten in één map (optioneel)
    print("Combineer mappen...")
    folderCombiner.main(folder=output_folder)

    print("Klaar! Alle bestanden verwerkt in:", output_folder)

if __name__ == "__main__":
    main()
