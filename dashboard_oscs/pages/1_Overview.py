import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.visualizations import plot_pie_chart, plot_bar_chart

st.set_page_config(page_title="Overview", layout="wide")

st.title("Visão Geral")

# Load Data
df = load_data()

if df.empty:
    st.error("Erro ao carregar os dados. Verifique se o arquivo data/oscs_santos.csv existe.")
else:
    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    
    total_oscs = len(df)
    ativas = len(df[df['situacao_cadastral'] == 'Ativa'])
    
    # Total de OS (Organizações Sociais - Código 3301)
    total_os = len(df[df['cd_natureza_juridica_osc'] == 3301]) if 'cd_natureza_juridica_osc' in df.columns else 0

    # Inicializar estado da seleção se não existir
    if 'selected_metric' not in st.session_state:
        st.session_state['selected_metric'] = None

    # Botões para interação
    if col1.button("Ver Lista", key="btn_total"):
        st.session_state['selected_metric'] = 'total'
    col1.metric("Total de OSCs", total_oscs)
    
    if col2.button("Ver Lista", key="btn_ativas"):
        st.session_state['selected_metric'] = 'ativas'
    col2.metric("OSCs Ativas", ativas)

    if col3.button("Ver Lista", key="btn_os"):
        st.session_state['selected_metric'] = 'os'
    col3.metric("Total de OS", total_os)

    # Exibição Condicional da Tabela
    if st.session_state['selected_metric']:
        st.divider()
        st.subheader("Detalhamento da Métrica Selecionada")
        
        detail_df = pd.DataFrame()
        
        if st.session_state['selected_metric'] == 'total':
            st.info("Mostrando todas as OSCs.")
            detail_df = df
            
        elif st.session_state['selected_metric'] == 'ativas':
            st.info("Mostrando apenas OSCs com situação cadastral Ativa.")
            detail_df = df[df['situacao_cadastral'] == 'Ativa']
        
        elif st.session_state['selected_metric'] == 'os':
            st.info("Mostrando apenas Organizações Sociais (Código 3301).")
            if 'cd_natureza_juridica_osc' in df.columns:
                detail_df = df[df['cd_natureza_juridica_osc'] == 3301]
            else:
                detail_df = pd.DataFrame()

        # Display table with dynamic height
        if not detail_df.empty:
            height = min((len(detail_df) + 1) * 35 + 3, 600) # Capping at 600px to avoid massive pages
            st.dataframe(detail_df, use_container_width=True, height=height)
            
            if st.button("Fechar Lista"):
                st.session_state['selected_metric'] = None
                st.rerun()
        else:
            st.warning("Nenhum registro encontrado para esta métrica.")

    st.divider()

    # --- Charts ---
    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Natureza Jurídica")
        if 'cd_natureza_juridica_osc' in df.columns:
            # Fallback mapping for common CSOs
            nat_jur_mapping = {
                3999: "Associação Privada",
                3069: "Fundação Privada",
                3220: "Organização Religiosa",
                3301: "Organização Social (OS)",
                2062: "Sociedade Empresária Limitada",
                2143: "Cooperativa",
                2135: "Empresário Individual",
                2305: "Empresa Individual de Resp. Limitada (Natureza Empresária)",
                2313: "Empresa Individual de Resp. Limitada (Natureza Simples)"
            }
            
            # Create a new column with mapped values, keeping original if not found
            df['Natureza_Juridica_Desc'] = df['cd_natureza_juridica_osc'].map(nat_jur_mapping).fillna(df['cd_natureza_juridica_osc'])
            
            fig_pie = plot_pie_chart(df, 'Natureza_Juridica_Desc', title="Distribuição por Natureza Jurídica")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Coluna de Natureza Jurídica não encontrada.")

    with c2:
        # st.subheader("OSCs por Ano de Fundação (Top 20)")
        if 'Ano_Fundacao' in df.columns:
            # Filtrar anos válidos
            df_year = df.dropna(subset=['Ano_Fundacao'])
            counts = df_year['Ano_Fundacao'].astype(int).value_counts().sort_index()
            # Plotar linha ou barra? Barra é melhor para distribuição discreta.
            # Vou plotar os ultimos 50 anos ou tudo?
            fig_bar = plot_bar_chart(df_year, 'Ano_Fundacao', title="Distribuição por Ano de Fundação", orientation='v')
            st.plotly_chart(fig_bar, use_container_width=True)
