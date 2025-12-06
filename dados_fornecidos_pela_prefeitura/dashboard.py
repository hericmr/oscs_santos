
import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.charts import plot_evolution_by_year, plot_top_beneficiaries, plot_by_secretariat

# Page Configuration
st.set_page_config(
    page_title="Análise OSCs Santos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for "Academic" Light Mode (Enforcing simple, clean look)
st.markdown("""
<style>
    .reportview-container {
        background: #ffffff;
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
    h1, h2, h3 {
        font-family: 'Times New Roman', Times, serif;
        color: #333;
    }
    p, div, label {
        font-family: 'Arial', sans-serif;
        color: #000;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Painel de Controle Social - OSCs Santos")
    st.markdown("Análise de repasses públicos para Organizações da Sociedade Civil.")

    # Load Data
    with st.spinner('Carregando dados...'):
        df = load_data()

    if df.empty:
        st.error("Não foi possível carregar os dados. Verifique se os arquivos CSV estão na pasta 'dados_completos'.")
        return

    # Sidebar Filters
    st.sidebar.header("Filtros")
    
    all_years = sorted(df['ano'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Selecione o Ano (ou Todos)", ["Todos"] + list(all_years))
    
    if selected_year != "Todos":
        df_filtered = df[df['ano'] == selected_year]
    else:
        df_filtered = df

    # Search by OSC
    search_osc = st.sidebar.text_input("Buscar por OSC (Nome)")
    if search_osc:
        df_filtered = df_filtered[df_filtered['beneficiaria_nome'].str.contains(search_osc, case=False, na=False)]

    # --- KPI Metrics ---
    total_repassado = df_filtered['valor_repasse'].sum()
    total_oscs = df_filtered['beneficiaria_id'].nunique()
    total_projetos = df_filtered['id'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Repassado", f"R$ {total_repassado:,.2f}")
    col2.metric("OSCs Beneficiadas", total_oscs)
    col3.metric("Projetos/Repasses", total_projetos)

    st.markdown("---")

    # --- Charts Section ---
    
    # Row 1: Evolution and Secretariat Distribution
    c1, c2 = st.columns(2)
    
    with c1:
        if selected_year == "Todos":
            st.plotly_chart(plot_evolution_by_year(df), use_container_width=True)
        else:
            st.info("Visualização 'Evolução por Ano' disponível apenas quando 'Todos' os anos estão selecionados.")
            
    with c2:
        st.plotly_chart(plot_by_secretariat(df_filtered), use_container_width=True)

    # Row 2: Top Beneficiaries
    st.plotly_chart(plot_top_beneficiaries(df_filtered), use_container_width=True)

    # --- Data Table Section ---
    st.markdown("### Dados Detalhados")
    with st.expander("Visualizar Dados Brutos"):
        st.dataframe(df_filtered)
        
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv,
            "dados_filtrados.csv",
            "text/csv",
            key='download-csv'
        )

if __name__ == "__main__":
    main()
