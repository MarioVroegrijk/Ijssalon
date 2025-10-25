import pandas as pd

def lees_en_valideer(file_path):
    """
    Leest het Excel-bestand met buigstaatregels en valideert verplichte kolommen.
    Verplichte kolommen: 'Ø', 'Lengte', 'Vormcode'
    """
    df = pd.read_excel(file_path)
    
    # Controleer of verplichte kolommen aanwezig zijn
    required_columns = ['Ø', 'Lengte', 'Vormcode']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Verplichte kolom ontbreekt: {col}")
    
    return df
