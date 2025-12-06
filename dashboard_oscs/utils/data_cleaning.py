import pandas as pd
import numpy as np

def clean_data(df):
    """
    Realiza a limpeza e preprocessamento dos dados.
    """
    # 1. Converter datas
    if 'dt_fundacao_osc' in df.columns:
        df['dt_fundacao_osc'] = pd.to_datetime(df['dt_fundacao_osc'], errors='coerce')
        df['Ano_Fundacao'] = df['dt_fundacao_osc'].dt.year

    # 2. Limpar Coordenadas (Latitude e Longitude)
    # As vezes vem com vírgula decimal, as vezes ponto.
    for col in ['latitude', 'longitude']:
        if col in df.columns:
            # Converter para string, substituir vírgula por ponto, e converter para numérico
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Processar Áreas de Atuação (One-Hot Decoding)
    # Colunas que começam com 'Area_'
    area_cols = [c for c in df.columns if c.startswith('Area_')]
    
    def get_primary_area(row):
        active_areas = []
        for col in area_cols:
            if row[col] == 1.0:
                # Remover prefixo 'Area_' e substituir underscores por espaços
                area_name = col.replace('Area_', '').replace('_', ' ')
                active_areas.append(area_name)
        
        if len(active_areas) == 0:
            return 'Não Informado'
        elif len(active_areas) == 1:
            return active_areas[0]
        else:
            return 'Múltiplas Áreas'

    if area_cols:
        df['Area_Atuacao'] = df.apply(get_primary_area, axis=1)

    # 4. Situação Cadastral
    if 'situacao_cadastral' in df.columns:
        df['situacao_cadastral'] = df['situacao_cadastral'].fillna('Desconhecida')

    return df
