
import sys
import os
import pandas as pd

# Mocking streamlit
class MockSt:
    def cache_data(self, func):
        return func
    def error(self, msg):
        print(f"ST ERROR: {msg}")
    def write(self, *args, **kwargs):
        pass # print(args)
    def caption(self, *args):
        pass

sys.modules['streamlit'] = MockSt()
import streamlit as st

# Add parent directory to path
sys.path.append('/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dashboard_oscs')
from dashboard_utils.data_loader import load_csv_robust

def verify():
    print("Verifying Tabela 6.2 Logic...")
    
    current_dir = '/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dashboard_oscs/pages'
    data_path_subarea = os.path.join(current_dir, '..', '..', 'dados atualizados', 'dados_filtrados', 'area_subarea.csv')
    
    if not os.path.exists(data_path_subarea):
        print(f"Data file not found at {data_path_subarea}")
        return

    df_sub = load_csv_robust(data_path_subarea)
    print(f"Loaded {len(df_sub)} rows from area_subarea.csv")
    
    def find_col(partial_name):
        matches = [c for c in df_sub.columns if partial_name in c]
        return matches[0] if matches else None

    # Simplified structure extract from the page code
    structure = [
        {"Area": "Habitação", "ColPai": "Habita", "Subareas": [("Habitação", "Hab sub Habita"), ("Outros Habitação", "Hab sub Outros")]},
        {"Area": "Desenvolvimento", "ColPai": "Desenvolvimento e defesa de direitos", 
         "Subareas": [("Associações de moradores", "Desenv e Def sub AssociaÃ§Ãµes de moradores")]},
         # Add more if needed for spot check
    ]

    print("\n--- DEEP DIVE HABITA ---")
    hab_cols = [c for c in df_sub.columns if "Habita" in c]
    for c in hab_cols:
        count = pd.to_numeric(df_sub[c], errors='coerce').sum()
        print(f"Col: {c} | Count: {count} | Uniques: {df_sub[c].unique()}")
        
    for item in structure:
        print(f"\nChecking Main Area: {item['Area']}")
        real_col_pai = find_col(item['ColPai'])
        if real_col_pai:
            # Check unique values
            uniques = df_sub[real_col_pai].unique()
            print(f"  Parent Col: {real_col_pai}")
            print(f"  Unique Values: {uniques}")
            
            count = pd.to_numeric(df_sub[real_col_pai], errors='coerce').sum()
            print(f"  Count (Sum): {count}")
            
            for sub_label, sub_partial in item["Subareas"]:
                real_col_sub = find_col(sub_partial)
                if real_col_sub:
                    sub_uniques = df_sub[real_col_sub].unique()
                    print(f"    Subarea: {sub_label} | Col: {real_col_sub} | Uniques: {sub_uniques}")
                    sub_count = pd.to_numeric(df_sub[real_col_sub], errors='coerce').sum()
                    print(f"    Count: {sub_count}")
                else:
                    print(f"    ❌ Subarea Col not found for: {sub_partial}")
        else:
             print(f"  ❌ Parent Col not found for: {item['ColPai']}")

if __name__ == "__main__":
    verify()
