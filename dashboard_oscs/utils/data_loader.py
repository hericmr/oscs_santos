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
