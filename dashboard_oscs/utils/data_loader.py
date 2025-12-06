import pandas as pd
import streamlit as st
import os
from utils.data_cleaning import clean_data

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

    try:
        # Tenta detectar separador automaticamente ou usa ; que é comum no Brasil
        try:
             df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        except:
             df = pd.read_csv(file_path, sep=',', encoding='utf-8')
        
        # Se houver erro de encoding, tentar latin1
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, sep=';', encoding='latin1')

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
            
            try:
                df = pd.read_csv(filepath, sep=',', encoding='utf-8')
            except:
                 df = pd.read_csv(filepath, sep=';', encoding='utf-8')
            
            df['ano'] = ano
            dfs.append(df)
        except Exception as e:
            st.warning(f"Erro ao ler arquivo {filename}: {e}")
            continue
            
    if not dfs:
        return pd.DataFrame()
        
    final_df = pd.concat(dfs, ignore_index=True)
    return final_df
