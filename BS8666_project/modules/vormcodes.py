import pandas as pd

vormcodes = {
    "00": {"beschrijving": "Rechte staaf", "params": ["A"]},
    "01": {"beschrijving": "Staaf met één haak 180°", "params": ["A"]},
    "11": {"beschrijving": "L-staaf 90°", "params": ["A","B"]},
    "12": {"beschrijving": "L-staaf 135° haak", "params": ["A","B"]},
    "99": {"beschrijving": "Vrije vorm (CAD input vereist)", "params": ["A"]},
}

def get_vormcodes_df():
    df = pd.DataFrame([
        {"Vormcode": code,
         "Beschrijving": data["beschrijving"],
         "Parameters": ", ".join(data["params"])}
        for code, data in vormcodes.items()
    ])
    return df
