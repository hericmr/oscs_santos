import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.visualizations import plot_pie_chart, plot_bar_chart


from utils.styles import apply_academic_style
apply_academic_style()

st.title("Visão Geral")

# Load Data
df = load_data()

if df.empty:
    st.error("Erro ao carregar os dados. Verifique se o arquivo data/oscs_santos.csv existe.")
else:
    # --- Principais Resultados ---
    from utils.components import render_key_results, render_employment_stats, render_kpis_section, render_table_6_3
    render_key_results(df)
    # render_employment_stats(df) # Hidden due to missing RAIS data
        
    # --- KPIs Section ---
    render_kpis_section(df)

    # --- Tabela 6.3 (IPEA) ---
    render_table_6_3(df)

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
            }
            df['Natureza_Juridica_Desc'] = df['cd_natureza_juridica_osc'].map(nat_jur_mapping).fillna(df['cd_natureza_juridica_osc'])
            fig_pie = plot_pie_chart(df, 'Natureza_Juridica_Desc', title="Distribuição por Natureza Jurídica")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Dados de Natureza Jurídica indisponíveis.")

    with c2:
        st.subheader("Ano de Fundação")
        if 'Ano_Fundacao' in df.columns:
            # Filtrar anos válidos
            df_year = df.dropna(subset=['Ano_Fundacao'])
            counts = df_year['Ano_Fundacao'].astype(int).value_counts().sort_index()
            # Plotar linha ou barra? Barra é melhor para distribuição discreta.
            # Vou plotar os ultimos 50 anos ou tudo?
            fig_bar = plot_bar_chart(df_year, 'Ano_Fundacao', title="Distribuição por Ano de Fundação", orientation='v')
            st.plotly_chart(fig_bar, use_container_width=True)
