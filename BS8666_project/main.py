import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Voeg projectmap toe aan sys.path
project_path = r"C:\Users\0031026\OneDrive - DEME\Documents\Mario Vroegrijk\Mario projecten\BS8666_project"
if project_path not in sys.path:
    sys.path.append(project_path)

# Modules importeren
from modules import vormcodes, berekening, excel_export, pdf_export

# Output bestanden
output_excel = os.path.join(project_path, "output", "buigstaten.xlsx")
output_pdf = os.path.join(project_path, "output", "buigstaten.pdf")

# ---------------- DataFrames ---------------- #
df_buigstaat = pd.DataFrame(columns=["Staafnr","Ø","Aantal","Lengte","Vormcode","Gewicht","Totaalgewicht"])

# Projectinformatie
project_info = {}

# ---------------- Functies ---------------- #

def start_buigstaat():
    # Verzamel projectinfo uit startscherm
    fields = ["Project","Deelproject","Onderdeel","Subonderdeel","Tekeningnr","Buigstaatnr"]
    for field in fields:
        value = start_entries[field].get()
        if value.strip() == "":
            messagebox.showerror("Fout", f"Vul {field} in.")
            return
        project_info[field] = value.strip()
    start_window.destroy()
    root.deiconify()  # Toon hoofd-GUI

def voeg_regel_toe():
    try:
        staafnr = entry_staafnr.get().strip()
        o_diameter = float(entry_diameter.get())
        aantal = int(entry_aantal.get())
        lengte = float(entry_lengte.get())
        code = combo_vormcode.get()
        if code == "":
            messagebox.showerror("Fout", "Selecteer een vormcode.")
            return

        # Bereken gewicht van één staaf
        df_tmp = pd.DataFrame([[o_diameter, lengte, code]], columns=["Ø","Lengte","Vormcode"])
        df_tmp_result = berekening.verwerk(df_tmp, vormcodes.vormcodes)
        gewicht = df_tmp_result.at[0, "Gewicht"] if "Gewicht" in df_tmp_result.columns else 0
        totaalgewicht = gewicht * aantal

        df_buigstaat.loc[len(df_buigstaat)] = [staafnr,o_diameter,aantal,lengte,code,gewicht,totaalgewicht]
        update_tabel()
        entry_staafnr.delete(0, tk.END)
        entry_diameter.delete(0, tk.END)
        entry_aantal.delete(0, tk.END)
        entry_lengte.delete(0, tk.END)
        combo_vormcode.set("")
    except ValueError:
        messagebox.showerror("Fout", "Controleer Ø, Aantal en Lengte.")

def update_tabel():
    table_text.config(state="normal")
    table_text.delete("1.0", tk.END)
    if not df_buigstaat.empty:
        table_text.insert(tk.END, df_buigstaat.to_string(index=False))
    table_text.config(state="disabled")

def verwerk_en_exporteer():
    if df_buigstaat.empty:
        messagebox.showerror("Fout", "Geen regels toegevoegd.")
        return
    try:
        df_result = berekening.verwerk(df_buigstaat[["Ø","Lengte","Vormcode"]].copy(), vormcodes.vormcodes)
        # Voeg Totaalgewicht per staafnummer toe
        df_result["Aantal"] = df_buigstaat["Aantal"]
        df_result["Totaalgewicht"] = df_buigstaat["Totaalgewicht"]
        excel_export.schrijf_excel(df_result, output_excel, project_info)
        messagebox.showinfo("Klaar", f"Excel opgeslagen in:\n{output_excel}")
    except Exception as e:
        messagebox.showerror("Fout", str(e))

def genereer_pdf_knop():
    if df_buigstaat.empty:
        messagebox.showerror("Fout", "Geen regels toegevoegd.")
        return
    try:
        pdf_export.genereer_pdf(df_buigstaat, output_pdf, project_info)
        messagebox.showinfo("Klaar", f"PDF gegenereerd in:\n{output_pdf}")
    except Exception as e:
        messagebox.showerror("Fout", str(e))

# ---------------- Startscherm ---------------- #
start_window = tk.Tk()
start_window.title("Projectinformatie")
start_window.geometry("400x350")

start_entries = {}
fields = ["Project","Deelproject","Onderdeel","Subonderdeel","Tekeningnr","Buigstaatnr"]
for i, field in enumerate(fields):
    tk.Label(start_window, text=f"{field}:", anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(start_window, width=30)
    entry.grid(row=i, column=1, padx=10, pady=5)
    start_entries[field] = entry

tk.Button(start_window, text="Start Buigstaat", command=start_buigstaat,
          bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(row=len(fields), column=0, columnspan=2, pady=20)

# ---------------- Hoofd-GUI ---------------- #
root = tk.Tk()
root.title("BS 8666 Buigstatenprogramma")
root.geometry("1000x750")
root.configure(bg="#f0f0f0")
root.withdraw()  # verberg totdat projectinfo ingevuld

# Invoer frame
frame_input = tk.Frame(root, bg="#f0f0f0")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Staafnr:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
entry_staafnr = tk.Entry(frame_input, width=10)
entry_staafnr.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Ø:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
entry_diameter = tk.Entry(frame_input, width=10)
entry_diameter.grid(row=0, column=3, padx=5)

tk.Label(frame_input, text="Aantal:", bg="#f0f0f0").grid(row=0, column=4, padx=5)
entry_aantal = tk.Entry(frame_input, width=10)
entry_aantal.grid(row=0, column=5, padx=5)

tk.Label(frame_input, text="Lengte:", bg="#f0f0f0").grid(row=0, column=6, padx=5)
entry_lengte = tk.Entry(frame_input, width=10)
entry_lengte.grid(row=0, column=7, padx=5)

tk.Label(frame_input, text="Vormcode:", bg="#f0f0f0").grid(row=0, column=8, padx=5)
combo_vormcode = ttk.Combobox(frame_input, values=list(vormcodes.vormcodes.keys()), width=10)
combo_vormcode.grid(row=0, column=9, padx=5)

tk.Button(frame_input, text="Regel toevoegen", command=voeg_regel_toe, bg="#2196F3", fg="white").grid(row=0, column=10, padx=10)

# Tabel voor ingevoerde regels + live gewicht
frame_table = tk.Frame(root)
frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame_table)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table_text = tk.Text(frame_table, yscrollcommand=scrollbar.set, wrap=tk.NONE, font=("Courier", 10), height=15, state="disabled")
table_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=table_text.yview)

# Knoppen voor Excel en PDF
tk.Button(root, text="Verwerk en exporteer naar Excel", command=verwerk_en_exporteer,
          bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

tk.Button(root, text="Genereer PDF-buigstaat", command=genereer_pdf_knop,
          bg="#FF9800", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

# Scrollable vormcodetabel
frame_vormcodes = tk.Frame(root)
frame_vormcodes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar2 = tk.Scrollbar(frame_vormcodes)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

text_vormcodes = tk.Text(frame_vormcodes, yscrollcommand=scrollbar2.set, wrap=tk.NONE, font=("Courier", 10))
text_vormcodes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar2.config(command=text_vormcodes.yview)

df_vormcodes = vormcodes.get_vormcodes_df()
text_vormcodes.insert(tk.END, df_vormcodes.to_string(index=False))
text_vormcodes.config(state="disabled")

root.mainloop()
