import os
import re
import pandas as pd
from PyPDF2 import PdfReader

# Map met PDF-bestanden
pdf_folder = "pad/naar/jouw/pdf_map"

# Lijst om originele tabel op te slaan
original_data = []

# Dictionary om samenvatting op te slaan per Staal
summary_data = {}

# Functie om velden uit PDF-tekst te halen
def extract_values(text):
    deel_match = re.search(r'Deel\s*[:\-]?\s*(\S+)', text)
    wap_match = re.search(r'Wap\.Tek\s*[:\-]?\s*(\S+)', text)
    plan_match = re.search(r'Plan Nr\.?\s*[:\-]?\s*(\S+)', text)
    zone_match = re.search(r'Zone\s*[:\-]?\s*(\S+)', text)
    # Staal: neem exacte waarde uit de PDF
    staal_match = re.search(r'Staal\s*[:\-]?\s*(.+)', text)
    staal = staal_match.group(1).strip() if staal_match else ""

    return {
        "Deel": deel_match.group(1) if deel_match else "",
        "Wap.Tek": wap_match.group(1) if wap_match else "",
        "Plan Nr.": plan_match.group(1) if plan_match else "",
        "Zone": zone_match.group(1) if zone_match else "",
        "Staal": staal
    }

# Functie om gewichten per Ø-diameter te halen
def extract_weights(text, staal):
    # Zoek alle regels die beginnen met 'tot. gew in kg' gevolgd door Ø en gewicht
    pattern = r'tot\. gew in kg\s*Ø\s*(\d+)\s*=\s*([\d\.]+)'
    matches = re.findall(pattern, text)
    for diameter, gewicht in matches:
        if staal not in summary_data:
            summary_data[staal] = {}
        if diameter in summary_data[staal]:
            summary_data[staal][diameter] += float(gewicht)
        else:
            summary_data[staal][diameter] = float(gewicht)

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
            original_data.append(values)
            extract_weights(text, values["Staal"])

# Maak originele tabel DataFrame
df_original = pd.DataFrame(original_data)

# Maak samenvatting DataFrame met Ø-diameters als kolommen
# Eerst alle unieke diameters verzamelen
all_diameters = set()
for staal_dict in summary_data.values():
    all_diameters.update(staal_dict.keys())
sorted_diameters = sorted(all_diameters, key=lambda x: int(x))

# Bouw samenvattingstabel
summary_rows = []
for staal, diam_dict in summary_data.items():
    row = {"Staal": staal}
    for dia in sorted_diameters:
        row[f"Ø{dia}"] = diam_dict.get(dia, 0)
    summary_rows.append(row)

df_summary = pd.DataFrame(summary_rows)

# Sla alles op in één Excel-bestand met twee sheets
with pd.ExcelWriter("output.xlsx") as writer:
    df_original.to_excel(writer, sheet_name="Overzicht", index=False)
    df_summary.to_excel(writer, sheet_name="Samenvatting", index=False)

print("Klaar! Excel 'output.xlsx' aangemaakt met Overzicht en Samenvatting.")
