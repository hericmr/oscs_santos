import pandas as pd
import os
import sys

# Mock streamlit for loader reuse if needed, or just standard pd.read_csv
def analyze_outros_as():
    base_path = '/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos'
    path_sub = os.path.join(base_path, 'dados atualizados/dados_filtrados/area_subarea.csv')
    path_main = os.path.join(base_path, 'dados atualizados/oscs_santos.csv')
    
    # Load Subarea Data
    # We know the column is likely 'Ass Social sub Outros' but we need to find it exactly
    try:
        df_sub = pd.read_csv(path_sub, sep=';', encoding='latin1') # Assumption based on robust loader
        if 'id_osc' not in df_sub.columns:
            # Try comma
            df_sub = pd.read_csv(path_sub, sep=',', encoding='latin1')
    except:
        pass
        
    # Load Main Data
    df_main = pd.read_csv(path_main, sep=';', encoding='latin1', on_bad_lines='skip')
    
    print("\nColumns in Area Subarea:", df_sub.columns.tolist())
    
    # Identify the target column
    target_col = [c for c in df_sub.columns if 'Ass Social sub Outros' in c]
    if not target_col:
        target_col = [c for c in df_sub.columns if 'Assistencia' in c and 'Outros' in c]
        
    print(f"\nTarget Column Candidates: {target_col}")
    
    if target_col:
        col = target_col[0]
        # Filter IDs where this column is 1
        ids_outros = df_sub[df_sub[col] == 1]['id_osc'].tolist()
        print(f"\nFound {len(ids_outros)} records in 'Outros Assistência Social'")
        
        # Filter Main DF
        # Check ID column in main
        print("\n--- Linking IDs ---")
        print(f"Sample 'cd_identificador_osc' in Sub: {df_sub['cd_identificador_osc'].astype(str).head(3).tolist()}")
        print(f"Sample 'cnpj' in Main: {df_main['cnpj'].astype(str).head(3).tolist()}")
        
        # Try to clean and merge
        # Usually CNPJ is numeric string. 'id_osc' might be an internal IPEA ID. 'cd_identificador_osc' is typically CNPJ.
        
        df_sub['clean_id'] = pd.to_numeric(df_sub['cd_identificador_osc'], errors='coerce')
        df_main['clean_id'] = pd.to_numeric(df_main['cnpj'], errors='coerce')
        
        # Determine valid IDs from sub
        valid_ids = df_sub[df_sub[col] == 1]['clean_id'].tolist()
        
        df_filtered = df_main[df_main['clean_id'].isin(valid_ids)]
        print(f"Merged Linked Records: {len(df_filtered)}")
        
        # Analyze desc
        # Main file columns printed above: 'cnae' seems to be the code, maybe no description?
        # Let's check 'cnae' and 'tx_razao_social_osc'
        
        if 'cnae' in df_filtered.columns:
            print(f"\nTop 20 CNAE Codes in 'Outros Assistência Social':")
            print(df_filtered['cnae'].value_counts().head(20))
            
        print("\nTop 10 Organization Names (Sample):")
        print(df_filtered['tx_razao_social_osc'].head(10).tolist())

if __name__ == "__main__":
    analyze_outros_as()
