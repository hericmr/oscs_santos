import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Adicionar o diretório pai ao sys.path para permitir a importação de utils
# Isso permite rodar a página individualmente ou via dashboard.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utils.data_loader import load_funding_data

st.set_page_config(layout="wide", page_title="Repasses da Prefeitura")

st.title("Repasses da Prefeitura para OSCs")

st.markdown("""
Esta página apresenta os dados de repasses financeiros da Prefeitura de Santos para as Organizações da Sociedade Civil (OSCs), 
com base nos arquivos de prestação de contas disponibilizados.
""")

# Citação Obrigatória
st.info("Dados fornecidos pela prefeitura, acessados através [https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas](https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas)")

df = load_funding_data()

if df.empty:
    st.warning("Nenhum dado de repasse encontrado.")
else:
    # Sidebar filters
    st.sidebar.header("Filtros")
    
    anos_disponiveis = sorted(df['ano'].unique(), reverse=True)
    ano_selecionado = st.sidebar.selectbox("Selecione o Ano", ["Todos"] + list(anos_disponiveis))
    
    df_filtered = df.copy()
    if ano_selecionado != "Todos":
        df_filtered = df_filtered[df_filtered['ano'] == ano_selecionado]

    # Metrics
    total_repassed = df_filtered['valor_repasse'].sum()
    total_records = len(df_filtered)
    unique_entities = df_filtered['beneficiaria_nome'].nunique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Valor Total Repassado", f"R$ {total_repassed:,.2f}")
    c2.metric("Total de Repasses", total_records)
    c3.metric("Entidades Beneficiadas", unique_entities)

    st.markdown("---")

    # Visualizations
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Evolução dos Repasses por Ano")
        if ano_selecionado == "Todos":
            daily_trend = df.groupby('ano')['valor_repasse'].sum().reset_index()
            fig_trend = px.bar(daily_trend, x='ano', y='valor_repasse', title="Total Repassado por Ano", labels={'valor_repasse': 'Valor (R$)', 'ano': 'Ano'})
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
             st.info("Visualização anual disponível apenas quando 'Todos' os anos estão selecionados.")

    with col_chart2:
        st.subheader("Top 10 Entidades Beneficiadas")
        top_entities = df_filtered.groupby('beneficiaria_nome')['valor_repasse'].sum().reset_index().sort_values('valor_repasse', ascending=False).head(10)
        fig_top = px.bar(top_entities, x='valor_repasse', y='beneficiaria_nome', orientation='h', title="Top 10 Entidades por Valor Recebido", labels={'valor_repasse': 'Valor (R$)', 'beneficiaria_nome': 'Entidade'})
        fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("---")
    st.subheader("Detalhamento dos Dados")
    st.dataframe(df_filtered, use_container_width=True)
