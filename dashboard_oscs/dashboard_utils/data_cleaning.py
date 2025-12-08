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

    # 3. Processar Áreas de Atuação (One-Hot Decoding) and SubAreas
    # Garantir que colunas binárias sejam numéricas
    binary_cols = [c for c in df.columns if c.startswith('Area_') or c.startswith('SubArea_')]
    for col in binary_cols:
        # Converter para numérico, forçando erros para NaN
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Colunas que começam com 'Area_' para a lógica de One-Hot
    area_cols = [c for c in df.columns if c.startswith('Area_')]
    
    def get_primary_area(row):
        active_areas = []
        for col in area_cols:
            if row[col] == 1:
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

def extract_bairro(addr):
    """
    Extrai o bairro de um endereço formatado (ex: LOGRADOURO, NUM, COMPL, BAIRRO, CIDADE, UF).
    Heurística simples baseada na posição em relação a 'SANTOS'.
    """
    if not isinstance(addr, str): return "Não Identificado"
    parts = addr.split(',')
    try:
        # Procurar 'Santos'
        sanitized_parts = [p.strip().upper() for p in parts]
        if 'SANTOS' in sanitized_parts:
            idx = sanitized_parts.index('SANTOS')
            if idx > 0:
                possible_bairro = parts[idx-1].strip()
                # Se for número ou complemento curto, tenta voltar mais um
                if len(possible_bairro) < 3 and idx > 1:
                        return parts[idx-2].strip()
                return possible_bairro.title() # Capitalize
        # Fallback: pegar o item do meio se tiver tamanho suficiente
        if len(parts) >= 4:
            return parts[-3].strip().title()
    except:
        pass
    return "Não Identificado"
