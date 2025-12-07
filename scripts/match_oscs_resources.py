import pandas as pd
import glob
import os
from difflib import get_close_matches
import unicodedata

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    # Normalize unicode characters to ASCII
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return text.upper().strip()

def main():
    # Paths
    oscs_path = "/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dados atualizados/oscs_santos.csv"
    resources_pattern = "/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dados_fornecidos_pela_prefeitura/dados_completos/prestacao-contas_prestacao_valor-ano_ano_*.csv"
    output_dir = "/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dados atualizados"

    # Load OSCs registry
    print(f"Loading OSCs from {oscs_path}...")
    try:
        df_oscs = pd.read_csv(oscs_path, sep=';', encoding='utf-8')
    except UnicodeDecodeError:
        df_oscs = pd.read_csv(oscs_path, sep=';', encoding='latin1')
    
    # Create a normalized name column for matching
    df_oscs['normalized_name'] = df_oscs['tx_razao_social_osc'].apply(normalize_text)
    # Also consider fantasy name?
    df_oscs['normalized_fantasy'] = df_oscs['tx_nome_fantasia_osc'].apply(normalize_text)
    
    # Create a lookup dictionary: normalized_name -> original_name, cnpj
    # We prioritize Razao Social, but can map Fantasy Name to the same record
    osc_lookup = {}
    for idx, row in df_oscs.iterrows():
        n_name = row['normalized_name']
        n_fantasy = row['normalized_fantasy']
        
        if n_name:
            osc_lookup[n_name] = {'name': row['tx_razao_social_osc'], 'cnpj': row['cnpj'], 'normalized_match': n_name}
        if n_fantasy and n_fantasy not in osc_lookup:
             osc_lookup[n_fantasy] = {'name': row['tx_razao_social_osc'], 'cnpj': row['cnpj'], 'normalized_match': n_name} # Map fantasy to main name

    valid_osc_names = list(osc_lookup.keys())

    # Load Resources
    print(f"Loading Resources files...")
    all_files = glob.glob(resources_pattern)
    
    resource_dfs = []
    for f in all_files:
        df = pd.read_csv(f)
        # Extract year from filename: ..._ano_2024.csv
        try:
            year = int(f.split('_ano_')[-1].split('.')[0])
        except (IndexError, ValueError):
            year = None
        df['ano_recurso'] = year
        resource_dfs.append(df)
        
    df_resources = pd.concat(resource_dfs, ignore_index=True)
    
    # Normalize resource beneficiary names
    df_resources['beneficiaria_nome_norm'] = df_resources['beneficiaria_nome'].apply(normalize_text)
    
    # Natureza Juridica Mapping
    natureza_map = {
        '3999': 'Associacao Privada',
        '3069': 'Fundacao Privada',
        '3220': 'Organizacao Religiosa',
        '3301': 'Organizacao Social (OS)',
        # Add others if needed based on data
    }

    # Matching Logic
    matched_data = []
    
    print("Starting matching process...")
    unique_resource_names = df_resources['beneficiaria_nome_norm'].unique()
    name_map = {} # resource_name_norm -> {matched_name, match_type, score, cnpj, natureza}

    for res_name in unique_resource_names:
        if not res_name:
            continue
            
        # 0. Manual Overrides (Specific User Requests)
        if "GALP" in res_name and "LAR POBRE" in res_name:
             # GALP - GRUPO AMIGO DO LAR POBRE -> GRUPO DE APOIO A INCLUSAO SOCIAL E PROFISSIONAL (CNPJ 58.258.633/0001-84)
             # We need to find this specific OSC in our lookup
             target_cnpj_root = "58258633" # First 8 digits usually enough to identify or find in lookup
             
             found_manual = None
             for name, info in osc_lookup.items():
                 if str(info['cnpj']).startswith(target_cnpj_root):
                     found_manual = info
                     break
             
             if found_manual:
                name_map[res_name] = {
                    'match_name': found_manual['name'],
                    'match_cnpj': found_manual['cnpj'],
                    'match_type': 'Manual (GALP)',
                    'score': 1.0
                }
                continue

        # 1. Exact Match
        if res_name in osc_lookup:
            match_info = osc_lookup[res_name]
            name_map[res_name] = {
                'match_name': match_info['name'],
                'match_cnpj': match_info['cnpj'],
                'match_type': 'Exact',
                'score': 1.0
            }
            continue

        # 3. Substring / Startswith Match
        # Check if any known name is a substring of resource name or vice versa
        found_substring = None
        best_sub_score = 0
        
        for name_key in valid_osc_names:
            # Check if name_key is in res_name
            # Avoid short matches like "A" or "OS" unless they are fantasy names verified
            if len(name_key) < 4:
                # Only if exact word match
                if f" {name_key} " in f" {res_name} ":
                     pass
                continue

            if name_key in res_name:
                # Calculate simple score based on length ratio
                score = len(name_key) / len(res_name)
                
                # Bonus for starting with the name
                if res_name.startswith(name_key):
                    score += 0.1
                
                if score > best_sub_score:
                    best_sub_score = score
                    found_substring = name_key
            
            # Check if res_name is in name_key
            elif res_name in name_key:
                score = len(res_name) / len(name_key)
                if name_key.startswith(res_name): # Bonus
                    score += 0.1
                    
                if score > best_sub_score:
                    best_sub_score = score
                    found_substring = name_key

        # Dynamic threshold based on length
        # exact substring of > 15 chars is very likely a match even if ratio is low (e.g. 50%)
        threshold = 0.6
        if found_substring and len(found_substring) > 15:
            threshold = 0.4
            
        if found_substring and best_sub_score > threshold:
             match_info = osc_lookup[found_substring]
             name_map[res_name] = {
                'match_name': match_info['name'],
                'match_cnpj': match_info['cnpj'],
                'match_type': 'Substring',
                'score': best_sub_score
            }
             continue
            
        # 4. Fuzzy Match
        # using difflib.get_close_matches to find potentially close matches
        matches = get_close_matches(res_name, valid_osc_names, n=1, cutoff=0.7) # Lowered to 0.7
        
        if matches:
            best_match = matches[0]
            # Calculate a similarity score (ratio) just for reporting
            from difflib import SequenceMatcher
            score = SequenceMatcher(None, res_name, best_match).ratio()
            
            match_info = osc_lookup[best_match]
            name_map[res_name] = {
                'match_name': match_info['name'],
                'match_cnpj': match_info['cnpj'],
                'match_type': 'Fuzzy',
                'score': score
            }
        else:
            name_map[res_name] = {
                'match_name': None,
                'match_cnpj': None,
                'match_type': 'None',
                'score': 0.0
            }

    # Apply comparisons back to dataframe
    def get_match_info(row):
        res_name = row['beneficiaria_nome_norm']
        if res_name in name_map:
            return pd.Series(name_map[res_name])
        return pd.Series({'match_name': None, 'match_cnpj': None, 'match_type': 'None', 'score': 0.0})

    match_columns = df_resources.apply(get_match_info, axis=1)
    df_final = pd.concat([df_resources, match_columns], axis=1)
    
    # Enrich with Natureza Juridica
    # create a dict cnpj -> natureza_cod
    cnpj_natureza = dict(zip(df_oscs['cnpj'], df_oscs['cd_natureza_juridica_osc']))
    
    def get_natureza(row):
        cnpj = row['match_cnpj']
        if pd.isna(cnpj):
            return None, None
        
        # handle float/str mismatch if necessary, assume cnpj is cleaner in df_oscs
        # df_oscs cnpj format: 11061656000211 (int or str)
        # match_cnpj might be float from the script earlier if not careful, but osc_lookup stores it from df_oscs row.
        
        nat_code = cnpj_natureza.get(cnpj)
        # Convert to string for safe lookup
        nat_desc = natureza_map.get(str(nat_code).replace('.0', ''), str(nat_code))
        return nat_code, nat_desc

    df_final[['cd_natureza_juridica', 'natureza_juridica_desc']] = df_final.apply(
        lambda row: pd.Series(get_natureza(row)), axis=1
    )

    # 3. Generate requested tables
    
    # Table 1: All Matches (matched + unmatched)
    output_all = os.path.join(output_dir, "tabela_recursos_osc_match_completo.csv")
    df_final.to_csv(output_all, index=False, sep=';', decimal=',')
    print(f"Saved complete table to {output_all}")

    # Table 2: Only Matched Resources
    df_matched_only = df_final[df_final['match_type'] != 'None']
    output_matched = os.path.join(output_dir, "tabela_recursos_osc_correspondidos.csv")
    df_matched_only.to_csv(output_matched, index=False, sep=';', decimal=',')
    print(f"Saved matched table to {output_matched}")

    # Table 3: Summary by OSC (Total Resources)
    # Group by the MATCHED name (or original if not matched, but let's focus on matched for the user request)
    # We will exclude unmatched for this specific summary to be clean
    # Include natureza_juridica_desc in the grouping or aggregation
    summary_osc = df_matched_only.groupby(['match_name', 'match_cnpj', 'natureza_juridica_desc'])['valor_repasse'].sum().reset_index()
    summary_osc = summary_osc.sort_values('valor_repasse', ascending=False)
    output_summary_osc = os.path.join(output_dir, "tabela_resumo_recursos_por_osc.csv")
    summary_osc.to_csv(output_summary_osc, index=False, sep=';', decimal=',')
    print(f"Saved summary by OSC to {output_summary_osc}")

    # Table 4: Unmatched names for manual review
    df_unmatched = df_final[df_final['match_type'] == 'None'][['beneficiaria_nome', 'beneficiaria_nome_norm', 'valor_repasse']].drop_duplicates()
    output_unmatched = os.path.join(output_dir, "relatorio_nomes_nao_correspondidos.csv")
    df_unmatched.to_csv(output_unmatched, index=False, sep=';', decimal=',')
    print(f"Saved unmatched report to {output_unmatched}")

if __name__ == "__main__":
    main()
