import streamlit as st
from utils.data_loader import load_data
from utils.visualizations import plot_bar_chart, plot_pie_chart

st.set_page_config(page_title="Situação Cadastral", layout="wide")

st.title("Situação Cadastral")

df = load_data()

if not df.empty and 'situacao_cadastral' in df.columns:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição Absoluta")
        fig_bar = plot_bar_chart(df, 'situacao_cadastral', title="Quantidade por Situação", orientation='v')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.subheader("Proporção")
        fig_pie = plot_pie_chart(df, 'situacao_cadastral', title="Percentual por Situação")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()
    
    # Cross analysis: Situação x Ano (Década?)
    if 'Ano_Fundacao' in df.columns:
        st.subheader("Situação Cadastral por Década de Fundação")
        df['Decada'] = (df['Ano_Fundacao'] // 10 * 10).astype('Int64').astype(str) + "s"
        
        import plotly.express as px
        # Group
        data_grouped = df.groupby(['Decada', 'situacao_cadastral']).size().reset_index(name='Quantidade')
        fig_cross = px.bar(data_grouped, x='Decada', y='Quantidade', color='situacao_cadastral', title="Situação por Década de Fundação", barmode='group')
        st.plotly_chart(fig_cross, use_container_width=True)

else:
    st.error("Dados de situação cadastral indisponíveis.")
