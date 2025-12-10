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

from dashboard_utils.data_loader import load_funding_data
from dashboard_utils.styles import apply_academic_style
from dashboard_utils.components import render_transfer_table_11_1


apply_academic_style()

st.title("Transferências de Recursos Públicos Municipais para OSs e OSCs")

render_transfer_table_11_1()

st.markdown("""
Esta página apresenta os dados de transferências de recursos públicos da Prefeitura de Santos para as Organizações da Sociedade Civil (OSCs), 
com base nos arquivos de prestação de contas disponibilizados.
""")

# Citação Obrigatória
st.info("Dados fornecidos pela prefeitura, acessados através [https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas](https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas)")

df = load_funding_data()

if df.empty:
    st.warning("Nenhum dado de transferência encontrado.")
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
    c1.metric("Valor Total Transferido", f"R$ {total_repassed:,.2f}")
    c2.metric("Total de Transferências", total_records)
    c3.metric("Entidades Beneficiadas", unique_entities)

    st.markdown("---")

    # Visualizations
    # Visualizations
    if ano_selecionado == "Todos":
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Evolução das Transferências por Ano")
            daily_trend = df.groupby('ano')['valor_repasse'].sum().reset_index()
            fig_trend = px.bar(daily_trend, x='ano', y='valor_repasse', title="Total Transferido por Ano", labels={'valor_repasse': 'Valor (R$)', 'ano': 'Ano'})
            st.plotly_chart(fig_trend, use_container_width=True)

        with col_chart2:
            st.subheader("Top 10 Entidades Beneficiadas (Geral)")
            top_entities = df_filtered.groupby('beneficiaria_nome')['valor_repasse'].sum().reset_index().sort_values('valor_repasse', ascending=False).head(10)
            fig_top = px.bar(top_entities, x='valor_repasse', y='beneficiaria_nome', orientation='h', title="Top 10 Entidades - Todos os Anos", labels={'valor_repasse': 'Valor (R$)', 'beneficiaria_nome': 'Entidade'})
            fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_top, use_container_width=True)
            
        st.markdown("---")
        st.subheader("Detalhamento dos Dados (Geral)")
        st.dataframe(df_filtered, use_container_width=True)

    else:
        st.subheader(f"Análise Detalhada de {ano_selecionado}")
        
        # --- Data Preparation ---
        
        # User requested to use 'Secretaria' instead of 'Área de Atuação'
        df_filtered['Secretaria'] = df_filtered['secretaria_sigla']
        target_col = 'Secretaria'

        
        # --- Charts ---

        # 1. Top 10 Entidades
        st.markdown("### 1. Top 10 Entidades com Maior Volume Transferido")
        top_10 = df_filtered.groupby('beneficiaria_nome')['valor_repasse'].sum().reset_index().nlargest(10, 'valor_repasse').sort_values('valor_repasse', ascending=True)
        fig_top10 = px.bar(top_10, x='valor_repasse', y='beneficiaria_nome', orientation='h', title=f"Top 10 Entidades - {ano_selecionado}", labels={'valor_repasse': 'Valor (R$)', 'beneficiaria_nome': 'Entidade'})
        st.plotly_chart(fig_top10, use_container_width=True)

        col_a, col_b = st.columns(2)
        
        with col_a:
            # 2. Pie Chart (Distribution by Area/Secretary)
            st.markdown(f"### 2. Distribuição por {target_col}")
            df_pie = df_filtered.groupby(target_col)['valor_repasse'].sum().reset_index()
            # Calculate percentages for legend similar to request
            total_val = df_pie['valor_repasse'].sum()
            df_pie['Percent'] = (df_pie['valor_repasse'] / total_val) * 100
            df_pie['Legend_Label'] = df_pie.apply(lambda x: f"{x[target_col]}: R$ {x['valor_repasse']:,.2f} ({x['Percent']:.1f}%)", axis=1)
            
            fig_pie = px.pie(df_pie, names='Legend_Label', values='valor_repasse', title=f"Distribuição de Verba por {target_col}")
            fig_pie.update_layout(showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            # 2.1 Bar Chart by Area
            st.markdown(f"### 3. Total por {target_col} (Barras)")
            df_bar_area = df_filtered.groupby(target_col)['valor_repasse'].sum().reset_index().sort_values('valor_repasse', ascending=False)
            fig_bar_area = px.bar(df_bar_area, x=target_col, y='valor_repasse', title=f"Total por {target_col}", labels={'valor_repasse': 'Valor (R$)'})
            st.plotly_chart(fig_bar_area, use_container_width=True)
            
        st.markdown("---")
        st.subheader("Tabela de Dados do Ano")
        st.dataframe(df_filtered, use_container_width=True)
