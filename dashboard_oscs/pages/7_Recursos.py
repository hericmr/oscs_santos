import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="Recursos", layout="wide")
from utils.styles import apply_academic_style
apply_academic_style()

st.title("Recursos e Financiamento")

# --- Helper Functions ---
@st.cache_data
def load_resources_data():
    """Load and merge resources data."""
    # Base paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', '..', 'dados atualizados', 'dados_filtrados')
    main_data_path = os.path.join(current_dir, '..', 'data', 'oscs_santos.csv')
    
    # 1. Load Main Data (OSCs Santos) to get names/valid IDs
    try:
        df_main = pd.read_csv(main_data_path, sep=';', dtype=str)
        # Clean CNPJ for joining
        df_main['cnpj_clean'] = df_main['cnpj'].str.replace(r'\D', '', regex=True)
    except Exception as e:
        st.error(f"Erro ao carregar oscs_santos.csv: {e}")
        return None, None

    # 2. Load 4786-recursososc.csv (IPEA Transferências)
    try:
        recursos_path = os.path.join(data_dir, '4786-recursososc.csv')
        df_recursos_ipea = pd.read_csv(recursos_path, sep=';', dtype=str)
        
        # Convert numeric columns
        df_recursos_ipea['nr_valor_recursos_osc'] = pd.to_numeric(df_recursos_ipea['nr_valor_recursos_osc'], errors='coerce').fillna(0)
        df_recursos_ipea['dt_ano_recursos_osc'] = pd.to_datetime(df_recursos_ipea['dt_ano_recursos_osc'], errors='coerce').dt.year
        
        # Join with Main Data on id_osc (or similar)
        # The file 4786 has 'id_osc' and 'cd_identificador_osc'. 
        # Typically 'cd_identificador_osc' is the CNPJ. Let's try joining on CNPJ first.
        # Clean column
        df_recursos_ipea['cnpj_join'] = df_recursos_ipea['cd_identificador_osc'].str.replace(r'\D', '', regex=True)
        
        # Merge to get Name and other info
        df_recursos_ipea = df_recursos_ipea.merge(
            df_main[['cnpj_clean', 'tx_razao_social_osc', 'situacao_cadastral']], 
            left_on='cnpj_join', 
            right_on='cnpj_clean', 
            how='inner' # Only keep matches in our filtered Santos set
        )
    except Exception as e:
        st.warning(f"Erro ao carregar 4786-recursososc.csv: {e}")
        df_recursos_ipea = pd.DataFrame()

    # 3. Load tb_recursos.csv (Ministério da Justiça)
    try:
        tb_recursos_path = os.path.join(data_dir, 'tb_recursos.csv')
        df_tb_recursos = pd.read_csv(tb_recursos_path, sep=';', dtype=str)
        
        # Clean CNPJ
        df_tb_recursos['cnpj_clean'] = df_tb_recursos['cnpj'].str.replace(r'\D', '', regex=True)
        
        # Clean percentages (replace % and comma)
        pct_cols = [c for c in df_tb_recursos.columns if '%' in str(df_tb_recursos[c].iloc[0]) or 'propria' in c or 'privada' in c or 'publica' in c]
        for col in pct_cols:
             if col in df_tb_recursos.columns:
                df_tb_recursos[col] = df_tb_recursos[col].str.replace('%', '').str.replace(',', '.').replace('', '0')
                df_tb_recursos[col] = pd.to_numeric(df_tb_recursos[col], errors='coerce').fillna(0)

        # Merge
        df_tb_recursos = df_tb_recursos.merge(
            df_main[['cnpj_clean', 'tx_razao_social_osc']], 
            on='cnpj_clean', 
            how='inner'
        )
    except Exception as e:
        st.warning(f"Erro ao carregar tb_recursos.csv: {e}")
        df_tb_recursos = pd.DataFrame()

    return df_recursos_ipea, df_tb_recursos

# --- Main Logic ---
df_ipea, df_mj = load_resources_data()

tab1, tab2 = st.tabs(["Repasses Federais (IPEA)", "Fontes de Recursos (MJ)"])

with tab1:
    st.header("Transferências Federais")
    st.markdown("Dados provenientes do Mapa das OSCs (IPEA) - Tabela `4786-recursososc.csv`.")
    
    if df_ipea is not None and not df_ipea.empty:
        # Metrics
        total_recursos = df_ipea['nr_valor_recursos_osc'].sum()
        st.metric("Total de Recursos Mapeados (R$)", f"{total_recursos:,.2f}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Evolução Temporal")
            df_year = df_ipea.groupby('dt_ano_recursos_osc')['nr_valor_recursos_osc'].sum().reset_index()
            fig_bar = px.bar(df_year, x='dt_ano_recursos_osc', y='nr_valor_recursos_osc', 
                             title="Volume de Recursos por Ano", labels={'dt_ano_recursos_osc':'Ano', 'nr_valor_recursos_osc':'Valor (R$)'})
            fig_bar.update_layout(xaxis_type='category')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            st.subheader("Fontes de Recursos")
            df_source = df_ipea['tx_nome_fonte_recursos_osc'].value_counts().reset_index()
            df_source.columns = ['Fonte', 'Quantidade']
            fig_pie = px.pie(df_source, names='Fonte', values='Quantidade', title="Distribuição por Fonte")
            st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("Detalhamento por OSC")
        st.dataframe(df_ipea[['dt_ano_recursos_osc', 'tx_razao_social_osc', 'nr_valor_recursos_osc', 'tx_nome_fonte_recursos_osc']].sort_values(by='dt_ano_recursos_osc', ascending=False), use_container_width=True)
    else:
        st.info("Não foram encontrados dados de repasses federais vinculados às OSCs de Santos nesta base.")

with tab2:
    st.header("Origem dos Recursos (Percentual)")
    st.markdown("Dados provenientes do Ministério da Justiça - Tabela `tb_recursos.csv`.")
    
    if df_mj is not None and not df_mj.empty:
        # Check available years
        years = sorted(df_mj['ano'].unique())
        selected_year = st.selectbox("Selecione o Ano", years)
        
        df_mj_year = df_mj[df_mj['ano'] == selected_year]
        
        st.subheader(f"Distribuição de Fontes em {selected_year}")
        
        # Select columns for visualization (numeric ones)
        resource_cols = ['propria_servico', 'propria_doacao_mensalidade', 'privada_doacao_parceria', 
                         'privada_doacao_even', 'publica_parceria', 'internacional_privada', 'internacional_publica']
        
        # Melt for visualization
        df_melt = df_mj_year.melt(id_vars=['tx_razao_social_osc'], value_vars=resource_cols, var_name='Tipo de Fonte', value_name='Percentual')
        
        # Filter out 0s for cleaner chart
        df_melt = df_melt[df_melt['Percentual'] > 0]
        
        fig_stack = px.bar(df_melt, x='tx_razao_social_osc', y='Percentual', color='Tipo de Fonte', 
                           title="Composição das Fontes de Recurso por OSC", barmode='stack')
        st.plotly_chart(fig_stack, use_container_width=True)

        st.subheader("Dados Detalhados")
        st.dataframe(df_mj_year, use_container_width=True)
    else:
         st.info("Não foram encontrados dados detalhados de fontes de recursos (MJ) para as OSCs de Santos.")
