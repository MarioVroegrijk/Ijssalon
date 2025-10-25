from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def genereer_pdf(df, output_path, project_info=None):
    """
    Genereert een PDF buigstaat met projectheader en totalen.
    df: DataFrame met kolommen Staafnr, Ø, Aantal, Lengte, Vormcode, Gewicht, Totaalgewicht
    project_info: dict met projectgegevens
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 50

    # Header met projectinfo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Buigstaat BS8666:2020")
    y -= 25
    if project_info:
        for key, value in project_info.items():
            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"{key}: {value}")
            y -= 20
    y -= 10

    # Kolom headers
    headers = ["Staafnr","Ø","Aantal","Lengte","Vormcode","Gewicht","Totaalgewicht"]
    x_positions = [50,100,150,200,270,350,420]
    c.setFont("Helvetica-Bold", 12)
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y, header)
    y -= 20
    c.setFont("Helvetica", 12)

    # Data
    for index, row in df.iterrows():
        for i, key in enumerate(headers):
            c.drawString(x_positions[i], y, str(row[key]))
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
            # herhaal header op nieuwe pagina
            c.setFont("Helvetica-Bold", 12)
            for i, header in enumerate(headers):
                c.drawString(x_positions[i], y, header)
            y -= 20
            c.setFont("Helvetica", 12)

    # Eventueel totalen per Ø
    totalen = df.groupby("Ø")["Totaalgewicht"].sum()
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Totalen per Ø:")
    y -= 20
    for diam, totaal in totalen.items():
        c.drawString(50, y, f"Ø {diam} mm: {totaal} kg")
        y -= 20

    c.save()
