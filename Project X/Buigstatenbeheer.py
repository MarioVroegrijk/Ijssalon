import os
import re
import pandas as pd
from PyPDF2 import PdfReader

# Map met PDF-bestanden
pdf_folder = "pad/naar/jouw/pdf_map"

# Lijst om resultaten op te slaan
data = []

# Functie om waarden uit PDF-tekst te halen
def extract_values(text):
    deel_match = re.search(r'Deel\s*[:\-]?\s*(\S+)', text)
    wap_match = re.search(r'Wap\.Tek\s*[:\-]?\s*(\S+)', text)
    plan_match = re.search(r'Plan Nr\.?\s*[:\-]?\s*(\S+)', text)
    zone_match = re.search(r'Zone\s*[:\-]?\s*(\S+)', text)

    # Staal = "Ja" als het woord Staal voorkomt, anders "Nee"
    staal = "Ja" if re.search(r'\bStaal\b', text, re.IGNORECASE) else "Nee"

    return {
        "Deel": deel_match.group(1) if deel_match else "",
        "Wap.Tek": wap_match.group(1) if wap_match else "",
        "Plan Nr.": plan_match.group(1) if plan_match else "",
        "Zone": zone_match.group(1) if zone_match else "",
        "Staal": staal
    }

# Loop door alle PDF's in de map
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(pdf_folder, filename)
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Alleen pagina's met tekst
                text += page_text + "\n"
        if text.strip():  # Alleen toevoegen als er bruikbare tekst is
            values = extract_values(text)
            data.append(values)

# Maak een DataFrame en sla op als Excel
df = pd.DataFrame(data)
df.to_excel("output.xlsx", index=False)
print("Klaar! Excel-bestand 'output.xlsx' is aangemaakt met de velden Deel, Wap.Tek, Plan Nr., Zone en Staal.")
