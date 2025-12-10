import sys
import os
import pandas as pd

# Add parent directory to path to import utils
sys.path.append('/home/hericmr/Documentos/Mapeamento cŕitico das organizações da sociedade civil em Santos/dashboard_oscs')

from dashboard_utils.data_loader import load_data

def debug():
    print("Loading data...")
    df = load_data()
    print(f"Data loaded: {len(df)} rows")
    
    hierarchy = {
        'Assistência Social': ['SubArea_Assistencia_social'],
        'Cultura e Recreação': ['SubArea_Cultura_e_arte', 'SubArea_Esportes_e_recreacao'],
        'Desenvolvimento e Defesa de Direitos': ['SubArea_Desenvolvimento_e_defesa_de_direitos'],
        'Educação e Pesquisa': ['SubArea_Educacao_infantil', 'SubArea_Ensino_fundamental', 'SubArea_Ensino_superior', 'SubArea_Educacao_profissional', 'SubArea_Atividades_de_apoio_a_educacao', 'SubArea_Outras_formas_de_educacao_ensino', 'SubArea_Estudos_e_pesquisas'],
        'Saúde': ['SubArea_Hospitais', 'SubArea_Outros_servicos_de_saude'],
        'Religião': ['SubArea_Religiao'],
        'Associações Patronais e Profissionais': ['SubArea_Associacoes_empresariais_e_patronais', 'SubArea_Associacoes_profissionais', 'SubArea_Associacoes_de_produtores_rurais_pescadores_e_similares'],
        'Outras Atividades Associativas': ['SubArea_Associacoes_de_atividades_nao_especificadas_anteriormente']
    }
    
    area_col_map = {
        'Area_Assistencia_social': 'Assistência Social',
        'Area_Cultura_e_recreacao': 'Cultura e Recreação',
        'Area_Desenvolvimento_e_defesa_de_direitos_e_interesses': 'Desenvolvimento e Defesa de Direitos',
        'Area_Educacao_e_pesquisa': 'Educação e Pesquisa',
        'Area_Saude': 'Saúde',
        'Area_Religiao': 'Religião',
        'Area_Associacoes_patronais_e_profissionais': 'Associações Patronais e Profissionais',
        'Area_Outras_atividades_associativas': 'Outras Atividades Associativas'
    }

    for area_col, area_name in area_col_map.items():
        print(f"\nChecking Area: {area_name} ({area_col})")
        if area_col not in df.columns:
            print(f"  ❌ Area Column {area_col} NOT FOUND in DF")
            continue
            
        parent_count = df[area_col].sum()
        print(f"  Parent Count: {parent_count}")
        
        subareas = hierarchy.get(area_name, [])
        for sub_col in subareas:
            if sub_col not in df.columns:
                print(f"  ❌ SubArea {sub_col} NOT FOUND in DF")
                continue
                
            total_sub = df[sub_col].sum()
            
            # The logic in the app:
            filtered_sub = df[df[area_col] == 1][sub_col].sum()
            
            print(f"  SubArea: {sub_col}")
            print(f"    Total in DF: {total_sub}")
            print(f"    Filtered (Parent==1): {filtered_sub}")
            
            if total_sub > 0 and filtered_sub == 0:
                print("    ⚠️ PROBLEM: SubArea has data but Parent is 0 for these rows!")

if __name__ == "__main__":
    debug()
