import pandas as pd
import streamlit as st
import os
from dashboard_utils.data_cleaning import clean_data


def load_csv_robust(filepath, decimal=','):
    """
    Tenta carregar um CSV lidando automaticamente com:
    - Encodings: utf-8, latin-1 (iso-8859-1)
    - Separadores: ;, ,, \t
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    separators = [';', ',', '\t']
    
    for encoding in encodings:
        for sep in separators:
            try:
                # Tenta ler apenas as primeiras linhas para validar
                df = pd.read_csv(filepath, sep=sep, encoding=encoding, nrows=5)
                # Se leu e tem colunas (>1 se sep correto, mas as vezes 1 coluna é válido, 
                # porem separadores errados costumam gerar 1 coluna com tudo junto)
                if len(df.columns) > 1:
                    # Ler arquivo inteiro
                    return pd.read_csv(filepath, sep=sep, encoding=encoding, decimal=decimal)
            except:
                continue
                
    # Se falhar tudo, tenta força bruta com o separador mais comum e latin1
    try:
        return pd.read_csv(filepath, sep=';', encoding='latin-1', decimal=decimal)
    except Exception as e:
        print(f"Erro ao carregar {filepath}: {e}")
        return pd.DataFrame()

@st.cache_data
def load_data(filename="oscs_santos.csv"):
    """
    Carrega os dados do CSV e aplica a limpeza.
    Usa cache do Streamlit para performance.
    O caminho é resolvido relativo à estrutura do projeto (../data/).
    """
    # Obter o diretório onde este script (data_loader.py) está localizado: /.../dashboard_oscs/utils/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Subir um nível para /.../dashboard_oscs/ e entrar em data/
    file_path = os.path.join(current_dir, '..', 'data', filename)

    if not os.path.exists(file_path):
        st.error(f"Arquivo não encontrado: {file_path}")
        return pd.DataFrame()

    df = load_csv_robust(file_path)

    df_cleaned = clean_data(df)
    return df_cleaned

@st.cache_data
def load_funding_data():
    """
    Carrega e consolida os dados de repasses da prefeitura.
    Lê arquivos do diretório data/prestacao_contas/ com padrão prestacao-contas_prestacao_valor-ano_ano_*.csv
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data', 'prestacao_contas')
    
    if not os.path.exists(data_dir):
        return pd.DataFrame()
        
    all_files = [f for f in os.listdir(data_dir) if f.startswith('prestacao-contas_prestacao_valor-ano_ano_') and f.endswith('.csv')]
    
    dfs = []
    for filename in all_files:
        filepath = os.path.join(data_dir, filename)
        try:
            # Extrair ano do nome do arquivo (esperado: ...ano_YYYY.csv)
            # O formato é prestacao-contas_prestacao_valor-ano_ano_2024.csv
            # Split por '_' e pegar o último elemento removendo .csv
            ano_str = filename.replace('.csv', '').split('_')[-1]
            ano = int(ano_str)
            
            df = load_csv_robust(filepath, decimal='.')
            
            if not df.empty:
                df['ano'] = ano
                dfs.append(df)
        except Exception as e:
            st.warning(f"Erro ao ler arquivo {filename}: {e}")
            continue
            
    if not dfs:
        return pd.DataFrame()
        
    final_df = pd.concat(dfs, ignore_index=True)
    return final_df
