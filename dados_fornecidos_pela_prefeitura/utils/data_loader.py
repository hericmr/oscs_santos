
import pandas as pd
import glob
import os
import re

DATA_PATH = "dados_completos"

def load_data():
    """
    Loads all 'prestacao-contas_prestacao_valor-ano_ano_*.csv' files,
    adds a 'ano' column based on the filename, and concatenates them.
    """
    all_files = glob.glob(os.path.join(DATA_PATH, "prestacao-contas_prestacao_valor-ano_ano_*.csv"))
    
    df_list = []
    
    for filename in all_files:
        try:
            # Extract year from filename (e.g., ..._ano_2024.csv)
            match = re.search(r"ano_(\d{4})\.csv", filename)
            if match:
                year = int(match.group(1))
            else:
                continue # Skip if year not found

            df = pd.read_csv(filename)
            df['ano'] = year
            df_list.append(df)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue

    if not df_list:
        return pd.DataFrame()

    final_df = pd.concat(df_list, ignore_index=True)
    
    # Ensure numeric columns are floats
    numeric_cols = ['valor_recurso', 'valor_repasse']
    for col in numeric_cols:
        if col in final_df.columns:
             # In case some files have string currency formatting (though we checked they seem clean)
             # We coerce errors just in case
             final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0.0)

    return final_df
