import os
import pandas as pd

def schrijf_excel(df, path):
    """
    Schrijft het DataFrame naar een Excel-bestand.
    Maakt de output-map automatisch aan als die niet bestaat.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_excel(path, index=False)
