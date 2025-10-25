def verwerk(df, codes):
    """
    Voert berekeningen uit op de buigstaatregels.
    Hier voegen we voorbeeldberekeningen toe:
    - Gewicht per Ø (dummyformule)
    - Totaal Gewicht
    """
    # Voeg kolom Gewicht per Ø toe
    df['Gewicht per Ø'] = df['Ø'] * 0.1  # voorbeeldformule
    
    # Voeg kolom Totaal Gewicht toe
    df['Totaal Gewicht'] = df['Gewicht per Ø'] * df['Lengte']
    
    return df
