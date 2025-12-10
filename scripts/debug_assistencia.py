import sys
import os
import pandas as pd

# Mock setup
class MockSt:
    def cache_data(self, func): return func
sys.modules['streamlit'] = MockSt()
sys.path.append('/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dashboard_oscs')
from dashboard_utils.data_loader import load_csv_robust

def debug_as():
    print("--- Debugging Assistência Social ---")
    current_dir = '/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dashboard_oscs/pages'
    data_path = os.path.join(current_dir, '..', '..', 'dados atualizados', 'dados_filtrados', 'area_subarea.csv')
    
    df = load_csv_robust(data_path)
    print(f"Loaded {len(df)} rows")
    
    # List all columns containing 'Assis' or 'Social'
    cols = [c for c in df.columns if 'Assis' in c or 'Social' in c]
    print("\nRelevant Columns found:")
    for c in cols:
        count = pd.to_numeric(df[c], errors='coerce').sum()
        print(f"  {c}: {count}")

    # Check the specific structure used in code
    print("\n--- Current Mapping Logic Checks ---")
    
    # Helper to mimic app logic
    def find_col(partial):
        matches = [c for c in df.columns if partial in c]
        return matches[0] if matches else None

    col_pai = find_col("AssistÃªncia social") # Note encoding from previous findings
    if not col_pai: col_pai = find_col("Assistência social")
    
    col_sub_outros = find_col("Ass Social sub Outros")
    col_sub_educa = find_col("Ass Social sub Educa") 
    col_sub_as = find_col("Ass Social sub AssistÃªncia social")

    print(f"Mapped Parent Col: {col_pai}")
    if col_pai: print(f"  Count: {pd.to_numeric(df[col_pai], errors='coerce').sum()}")
    
    print(f"Mapped Sub Outros: {col_sub_outros}")
    if col_sub_outros: print(f"  Count: {pd.to_numeric(df[col_sub_outros], errors='coerce').sum()}")

    print(f"Mapped Sub Educa: {col_sub_educa}")
    if col_sub_educa: print(f"  Count: {pd.to_numeric(df[col_sub_educa], errors='coerce').sum()}")

    print(f"Mapped Sub AS: {col_sub_as}")
    if col_sub_as: print(f"  Count: {pd.to_numeric(df[col_sub_as], errors='coerce').sum()}")

if __name__ == "__main__":
    debug_as()
