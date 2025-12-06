import streamlit as st
from streamlit_folium import st_folium
from utils.data_loader import load_data
from utils.visualizations import plot_map

st.set_page_config(page_title="Evolução Temporal", layout="wide")

st.title("Evolução Temporal no Mapa")

st.markdown("""
Mova a linha do tempo abaixo para visualizar o surgimento das OSCs em Santos ao longo dos anos.
""")

df = load_data()

if not df.empty and 'Ano_Fundacao' in df.columns:
    # Preparar dados
    df = df.dropna(subset=['Ano_Fundacao', 'latitude', 'longitude'])
    df['Ano_Fundacao'] = df['Ano_Fundacao'].astype(int)
    
    min_year = int(df['Ano_Fundacao'].min())
    max_year = int(df['Ano_Fundacao'].max())
    
    # Timeline Slider (Faixa de Tempo)
    # Permite selecionar (Inicio, Fim)
    range_anos = st.slider(
        "Selecione o Período",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    start_year, end_year = range_anos
    
    # Filtrar dados pelo range selecionado
    df_filtered = df[(df['Ano_Fundacao'] >= start_year) & (df['Ano_Fundacao'] <= end_year)]
    
    col1, col2 = st.columns(2)
    oscs_no_periodo = len(df_filtered)
    
    col1.metric(f"OSCs criadas entre {start_year} e {end_year}", oscs_no_periodo)
    
    if not df_filtered.empty:
        # Labels amigáveis
        cols_to_show = {
            'tx_razao_social_osc': 'Razão Social',
            'dt_fundacao_osc': 'Fundação',
            'Area_Atuacao': 'Área',
            'situacao_cadastral': 'Situação',
            'tx_endereco_completo': 'Endereço'
        }
        
        m = plot_map(df_filtered, tooltip_cols=cols_to_show)
        
        st_folium(m, width="100%", height=600)
    else:
        st.info("Nenhuma OSC encontrada até o ano selecionado.")

else:
    st.error("Dados insuficientes para gerar a evolução temporal.")
