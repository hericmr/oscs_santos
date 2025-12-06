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
    # Visualizations
    if ano_selecionado == "Todos":
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Evolução dos Repasses por Ano")
            daily_trend = df.groupby('ano')['valor_repasse'].sum().reset_index()
            fig_trend = px.bar(daily_trend, x='ano', y='valor_repasse', title="Total Repassado por Ano", labels={'valor_repasse': 'Valor (R$)', 'ano': 'Ano'})
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
        
        # Load Dictionary for Areas
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dict_path = os.path.join(current_dir, '..', '..', 'scripts', 'dicionario_secretarias.csv')
        
        if os.path.exists(dict_path):
            df_dict = pd.read_csv(dict_path)
            # Helper to get first dept (if comma separated)
            def get_first_dept(dept_str):
                if isinstance(dept_str, str):
                    return dept_str.split(',')[0].strip()
                return dept_str

            df_filtered['Secretaria_Principal'] = df_filtered['secretaria_sigla'].apply(get_first_dept)
            df_filtered = df_filtered.merge(df_dict[['Sigla', 'Área de Atuação']], left_on='Secretaria_Principal', right_on='Sigla', how='left')
            df_filtered['Área de Atuação'] = df_filtered['Área de Atuação'].fillna('Outros')
            target_col = 'Área de Atuação'
        else:
            st.warning("Dicionário de secretarias não encontrado. Classificação por Área de Atuação indisponível. Usando 'Secretaria'.")
            target_col = 'secretaria_sigla'

        
        # --- Charts ---

        # 1. Top 10 Entidades
        st.markdown("### 1. Top 10 Entidades com Maior Repasse")
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

        col_c, col_d = st.columns(2)
        
        with col_c:
            # 3. Histogram
            st.markdown("### 4. Histograma de Valores de Repasse")
            fig_hist = px.histogram(df_filtered, x='valor_repasse', nbins=30, title="Distribuição dos Valores de Repasse")
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col_d:
            # 4. Pareto Analysis
            st.markdown("### 5. Análise de Pareto")
            df_pareto = df_filtered.sort_values(by='valor_repasse', ascending=False)
            df_pareto['Acumulado'] = df_pareto['valor_repasse'].cumsum()
            df_pareto['Percentual Acumulado'] = 100 * df_pareto['Acumulado'] / df_pareto['valor_repasse'].sum()
            
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go
            
            fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
            
            limit_pareto = 50
            df_pareto_plot = df_pareto.head(limit_pareto)
            
            fig_pareto.add_trace(
                go.Bar(x=df_pareto_plot['beneficiaria_nome'], y=df_pareto_plot['valor_repasse'], name="Valor Repasse"),
                secondary_y=False
            )
            
            fig_pareto.add_trace(
                go.Scatter(x=df_pareto_plot['beneficiaria_nome'], y=df_pareto_plot['Percentual Acumulado'], name="% Acumulado", mode='lines+markers', marker=dict(color='orange')),
                secondary_y=True
            )
            
            fig_pareto.update_layout(title="Análise de Pareto (Top 50 Entidades)")
            fig_pareto.add_hline(y=80, line_dash="dash", line_color="gray", annotation_text="80%", secondary_y=True)
            st.plotly_chart(fig_pareto, use_container_width=True)

        # 5. WordCloud
        st.markdown("### 6. Nuvem de Palavras (Nome das Entidades)")
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            
            text = ' '.join(df_filtered['beneficiaria_nome'].astype(str))
            stopwords = ['DE', 'DA', 'DO', 'DOS', 'DAS', 'E', 'A', 'O', 'EM', 'PARA', 'COM', 'POR', 'SANTOS', 'ASSOCIAÇÃO', 'SOCIEDADE', 'INSTITUTO', 'CENTRO', 'GRUPO', 'GRÊMIO', 'APM', 'UME', 'OSC', 'ORGANIZAÇÃO', 'SERVIÇO', 'SOCIAL']
            
            wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
            
            fig_wc, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_wc)
        except ImportError:
            st.warning("Biblioteca 'wordcloud' não instalada. Visualização indisponível.")

        # 6. Bar Chart Total by Secretary (Pure)
        if target_col != 'secretaria_sigla':
            st.markdown("### 7. Total por Secretaria")
            df_sec = df_filtered.groupby('secretaria_sigla')['valor_repasse'].sum().reset_index().sort_values('valor_repasse', ascending=False)
            fig_sec = px.bar(df_sec, x='secretaria_sigla', y='valor_repasse', title="Total de Repasses por Secretaria", labels={'valor_repasse': 'Valor (R$)', 'secretaria_sigla': 'Secretaria'})
            st.plotly_chart(fig_sec, use_container_width=True)
            
        st.markdown("---")
        st.subheader("Tabela de Dados do Ano")
        st.dataframe(df_filtered, use_container_width=True)
