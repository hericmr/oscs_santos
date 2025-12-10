import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard_utils.styles import apply_academic_style

# Apply global styles
apply_academic_style()

st.title("Análise de Vínculos: OSCs vs RAIS 2023 (Santos)")

st.markdown("""
Dados sobre o trabalho nas Organizações da Sociedade Civil (OSCs) usando informações da Rais. A análise foca apenas nos empregos formais. Como a Rais não tem dados sobre voluntários, eles não foram incluídos. Os voluntários são uma parte importante das OSCs, por isso, o número real de pessoas trabalhando é maior do que o mostrado aqui. Além disso, a Rais só registra quem tem carteira assinada, deixando de fora os trabalhadores autônomos e informais.
""")

# --- Helper Functions ---
def clean_percentage(x):
    if isinstance(x, str):
        return float(x.replace('%', '').replace(',', '.'))
    return x

import os
from dashboard_utils.data_loader import load_csv_robust

# ...

@st.cache_data
def load_analysis_data():
    # Resolve path relative to this script:
    # dashboard_oscs/pages/10... -> up to dashboard_oscs -> up to root -> dados atualizados...
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, '..', '..', 'dados atualizados', 'dados_filtrados')
    
    def get_path(filename):
        return os.path.join(base_path, filename)

    try:
        # Using load_csv_robust for safer loading (encodings/separators)
        df_71 = load_csv_robust(get_path("tabela_7_1_pessoal_ocupado.csv"))
        df_72 = load_csv_robust(get_path("tabela_7_2_pessoal_por_area.csv"))
        df_73 = load_csv_robust(get_path("tabela_7_3_faixas_vinculos.csv"))
        df_82 = load_csv_robust(get_path("tabela_8_2_finalidade_x_faixas.csv"))
        return df_71, df_72, df_73, df_82
    except Exception as e:
        st.error(f"Erro ao carregar arquivos: {e}")
        return None, None, None, None

df_71, df_72, df_73, df_82 = load_analysis_data()

if df_71 is not None:
    
    # --- Tabela 7.1: Pessoal Ocupado ---
    st.subheader("Tabela 4 - Pessoal Ocupado por Natureza Jurídica")
    
    # Cleaning for chart
    df_71_plot = df_71[df_71['Natureza Jurídica'] != 'TOTAL'].copy()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.caption("Tabela 7.1: Pessoal Ocupado nas OSCs por Natureza Jurídica")
        # st.markdown(df_71.to_markdown(index=False)) 
        st.dataframe(df_71, hide_index=True)

    with col2:
        fig_71 = px.pie(
            df_71_plot, 
            values='Pessoal Ocupado', 
            names='Natureza Jurídica', 
            title='Distribuição do Pessoal Ocupado',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_71, use_container_width=True)

    st.divider()

    # --- Tabela 7.2: Pessoal por Área ---
    st.subheader("Tabela 5 - Pessoal Ocupado por Área de Atuação")
    
    df_72_plot = df_72[df_72['Finalidade de atuação'] != 'TOTAL'].copy()
    
    # Clean percentages for usage if needed, though we operate mostly on N for magnitude
    
    col3, col4 = st.columns([1, 1])
    with col3:
        st.caption("Tabela 7.2: OSCs e Pessoal Ocupado por Área de Atuação")
        st.dataframe(df_72, hide_index=True)
    
    with col4:
        # Comparison chart: Share of OSCs vs Share of Personnel?
        # Let's clean the percentages first
        df_72_plot['OSCs (%) Clean'] = df_72_plot['OSCs (%)'].apply(clean_percentage)
        df_72_plot['Pessoal (%) Clean'] = df_72_plot['Pessoal (%)'].apply(clean_percentage)

        # Melt for grouped bar chart
        df_melted = df_72_plot.melt(
            id_vars=['Finalidade de atuação'], 
            value_vars=['OSCs (%) Clean', 'Pessoal (%) Clean'],
            var_name='Métrica', 
            value_name='Porcentagem'
        )
        
        fig_72 = px.bar(
            df_melted,
            x='Porcentagem',
            y='Finalidade de atuação',
            color='Métrica',
            barmode='group',
            orientation='h',
            title='Comparativo: % OSCs vs % Pessoal',
            height=500
        )
        st.plotly_chart(fig_72, use_container_width=True)

    st.divider()

    # --- Tabela 7.3: Faixas de Vínculos ---
    st.subheader("Tabela 6 - Distribuição por Faixas de Vínculos")
    
    df_73_plot = df_73.copy()
    # Ensure correct order if it's categorical? It seems pre-sorted in file 1..10
    
    col5, col6 = st.columns([1, 1])
    with col5:
        st.caption("Tabela 7.3: Distribuição das OSCs por Faixas de Vínculos")
        st.dataframe(df_73, hide_index=True)
        
    with col6:
        fig_73 = px.bar(
            df_73_plot,
            x='Faixas de vínculos',
            y='N',
            text='N',
            title='Número de OSCs por Faixa de Vínculos',
            color_discrete_sequence=['#4c78a8']
        )
        st.plotly_chart(fig_73, use_container_width=True)

    st.divider()

    # --- Tabela 8.2: Finalidade x Faixas ---
    st.subheader("Tabela 7 - Finalidade das OSCs x Faixas de Vínculos")
    
    # We want to show the full table and maybe a heatmap of Counts (N)
    
    # Filter columns that are (N) count columns for the heatmap
    # Columns are: 'Finalidade das OSCs', 'Sem vínculos (N)', 'Sem vínculos (%)', ...
    # We ignore 'Total (N)' and 'Total (%)' for the heatmap usually to avoid skew, or keep them?
    # Usually exclude margins for heatmap.
    
    n_cols = [c for c in df_82.columns if '(N)' in c and 'Total' not in c]
    
    # Matrix for heatmap
    # We need to set index to Finalidade
    df_82_heatmap = df_82[df_82['Finalidade das OSCs'] != 'TOTAL'].set_index('Finalidade das OSCs')[n_cols]
    
    # Remove '(N)' from column names for cleaner display in chart
    df_82_heatmap.columns = [c.replace(' (N)', '') for c in df_82_heatmap.columns]
    
    st.caption("Tabela 8.2: Detalhamento por Finalidade e Faixa")
    st.dataframe(df_82, hide_index=True, use_container_width=True)
    
    st.write("### Mapa de Calor (Quantidade de OSCs)")
    fig_82 = px.imshow(
        df_82_heatmap,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Distribuição de Vínculos por Finalidade"
    )
    st.plotly_chart(fig_82, use_container_width=True)
