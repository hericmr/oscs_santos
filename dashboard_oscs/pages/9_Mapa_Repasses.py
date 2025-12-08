import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import plotly.express as px
from dashboard_utils.data_loader import load_data, load_csv_robust
from dashboard_utils.visualizations import plot_map, apply_academic_chart_style
from dashboard_utils.styles import apply_academic_style
import os


apply_academic_style()

st.title("Mapa 3 - Evolução Quantitativa das Transferências")
st.markdown("""
Esta página apresenta a evolução quantitativa das transferências e representações gráficas resultantes do cruzamento entre a base de dados do Mapa das OSCs (recorte: Santos) e os registros de prestação de contas da Prefeitura de Santos
""")

# --- Carregar Dados ---
# 1. Carregar dados financeiros (Matches)
current_dir = os.path.dirname(os.path.abspath(__file__))
match_file_path = os.path.join(current_dir, '..', 'data', 'tabela_recursos_osc_match_completo.csv')

@st.cache_data
def load_match_data():
    if not os.path.exists(match_file_path):
        return pd.DataFrame()
    
    return load_csv_robust(match_file_path)

df_matches = load_match_data()

# 2. Carregar dados de OSCs (Coordenadas)
df_oscs = load_data() # Returns df with 'cnpj', 'latitude', 'longitude'

if df_matches.empty or df_oscs.empty:
    st.error("Dados insuficientes para gerar a visualização geográfica.")
    st.stop()

# --- Preparação dos Dados ---

# Filtrar apenas matches válidos (não None)
df_valid_matches = df_matches[df_matches['match_type'].notna() & (df_matches['match_type'] != 'None')].copy()

# Converter colunas de repasse para float (se necessário)
def parse_currency(x):
    if isinstance(x, str):
        return float(x.replace('.', '').replace(',', '.'))
    return float(x) if x else 0.0

df_valid_matches['valor_repasse_float'] = df_valid_matches['valor_repasse'].apply(parse_currency)

# Garantir CNPJ limpo para merge
# df_oscs já deve ter 'cnpj' limpo pelo clean_data
# df_valid_matches 'match_cnpj' deve ser limpo
def clean_cnpj(x):
    if pd.isna(x): return ''
    s = str(x)
    # Remove decimal part if exists (e.g. 1234,0 -> 1234)
    if ',' in s:
        s = s.split(',')[0]
    elif '.' in s:
        s = s.split('.')[0]
    return ''.join(filter(str.isdigit, s))

df_valid_matches['match_cnpj_clean'] = df_valid_matches['match_cnpj'].apply(clean_cnpj)
df_oscs['cnpj_clean'] = df_oscs['cnpj'].apply(clean_cnpj)

# Merge para pegar coordenadas e detalhes
# Left merge no match para manter os repasses, trazendo coords do df_oscs
df_merged = df_valid_matches.merge(
    df_oscs[['cnpj_clean', 'latitude', 'longitude', 'tx_endereco_completo', 'situacao_cadastral', 'dt_fundacao_osc']],
    left_on='match_cnpj_clean',
    right_on='cnpj_clean',
    how='inner' # Inner para garantir que só mostramos quem tem coordenada
)

# Se latitude/longitude forem vazias, remover
df_merged = df_merged.dropna(subset=['latitude', 'longitude'])

# Extrair Bairro (Heurística simples: assumindo formato "Logradouro, Numero, Compl, Bairro, Cidade, UF")
def extract_bairro(addr):
    if not isinstance(addr, str): return "N/A"
    parts = addr.split(',')
    # Geralmente o bairro é o antepenúltimo ou antes de "Santos"
    # Ex: RUA X, 123, BAIRRO Y, SANTOS, SP
    try:
        # Procurar 'Santos'
        sanitized_parts = [p.strip().upper() for p in parts]
        if 'SANTOS' in sanitized_parts:
            idx = sanitized_parts.index('SANTOS')
            if idx > 0:
                possible_bairro = parts[idx-1].strip()
                # Se for número ou complemento curto, tenta voltar mais um
                if len(possible_bairro) < 3 and idx > 1:
                     return parts[idx-2].strip()
                return possible_bairro
        # Fallback: pegar o item do meio se tiver tamanho suficiente
        if len(parts) >= 4:
            return parts[-3].strip()
    except:
        pass
    return "N/A"

df_merged['Bairro'] = df_merged['tx_endereco_completo'].apply(extract_bairro)

# Garantir Ano como Inteiro
df_merged['ano_recurso'] = df_merged['ano_recurso'].fillna(0).astype(int)

# --- Filtro Temporal (Slider) ---
min_year = int(df_merged['ano_recurso'].min()) if not df_merged.empty else 2016
max_year = int(df_merged['ano_recurso'].max()) if not df_merged.empty else 2025

st.subheader("Linha do Tempo")
# Slider para selecionar intervalo (range)
year_range = st.slider("Selecione o Período", min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)
start_year, end_year = year_range

# Filtro
df_year = df_merged[(df_merged['ano_recurso'] >= start_year) & (df_merged['ano_recurso'] <= end_year)]

# --- Agregação por OSC para o Mapa ---
# Uma OSC pode ter recebido vários repasses no ano. Queremos 1 pino no mapa.
# Agrupar por CNPJ e manter dados estáticos da OSC
# Para o nome da beneficiária, pegamos o mais frequente (moda) ou o primeiro para exibir no tooltip
group_cols = ['match_cnpj_clean', 'match_name', 'latitude', 'longitude', 'cd_natureza_juridica', 'natureza_juridica_desc', 
              'situacao_cadastral', 'Bairro', 'dt_fundacao_osc', 'tx_endereco_completo']

# Função de agregação personalizada para pegar o nome da beneficiária mais comum
def get_most_common(x):
    try:
        return x.mode().iloc[0]
    except:
        return x.iloc[0] if not x.empty else "N/A"

# Função para agrupar secretarias únicas
def get_unique_secretarias(x):
    return ", ".join(sorted(x.astype(str).unique()))

df_map_data = df_year.groupby(group_cols).agg({
    'valor_repasse_float': 'sum',
    'id': 'count', # Contagem de repasses
    'beneficiaria_nome': get_most_common, # Trazer o nome usado no repasse
    'secretaria_sigla': get_unique_secretarias # Lista de secretarias
}).reset_index()

# Renomear para compatibilidade com plot_map OU criar dados de tooltip manuais
df_map_data.rename(columns={
    'match_name': 'tx_nome_fantasia_osc', # Para plot_map usar como titulo do popup
    'valor_repasse_float': 'Valor Total Recebido',
    'id': 'Qtd. Transferências',
    'cd_natureza_juridica': 'cd_natureza_juridica_osc', # Para cor (3301 = OS)
    'natureza_juridica_desc': 'Tipo Jurídico',
    'beneficiaria_nome': 'Beneficiária', # Nome que irá no tooltip hover
    'secretaria_sigla': 'Secretarias'
}, inplace=True)

# Formatar valor para tooltip
df_map_data['Valor Formatado'] = df_map_data['Valor Total Recebido'].apply(lambda x: f"R$ {x:,.2f}")

# --- Filtro de Pesquisa (Destaque no Mapa) ---
if not df_map_data.empty:
    osc_options = sorted(df_map_data['tx_nome_fantasia_osc'].astype(str).unique())
    selected_osc = st.selectbox("Pesquisar OSC por Nome (Filtrar Mapa)", ["Todas"] + osc_options)

    if selected_osc != "Todas":
        df_map_data = df_map_data[df_map_data['tx_nome_fantasia_osc'] == selected_osc]
        st.info(f"Exibindo destaque para: **{selected_osc}**")

# --- Renderização ---

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"### Mapa 3 - Distribuição das Transferências ({start_year} - {end_year})")
    
    if not df_map_data.empty:
        # Colunas para tooltip enriquecido (Popup)
        tooltip = {
            'Tipo Jurídico': 'Tipo',
            'Bairro': 'Bairro',
            'situacao_cadastral': 'Situação',
            'dt_fundacao_osc': 'Fundação',
            'Secretarias': 'Resp. Repasse',
            'Qtd. Transferências': 'Qtd. Transferências',
            'Valor Formatado': 'Valor Total'
        }
        
        # Hover mostra o nome da beneficiária (como solicitado)
        m = plot_map(df_map_data, tooltip_cols=tooltip, hover_name_col='Beneficiária')
        st_folium(m, width="100%", height=600)
    else:
        st.info(f"Nenhuma transferência mapeada com coordenadas para o período {start_year}-{end_year}.")

with col2:
    st.markdown("### Resumo do Período")
    
    # Métricas Simples
    total_val = df_map_data['Valor Total Recebido'].sum()
    qtd_oscs = df_map_data['match_cnpj_clean'].nunique()
    
    st.metric("Total Transferido", f"R$ {total_val:,.2f}")
    st.metric("OSCs Beneficiadas", qtd_oscs)
    
    
    # Detalhe removido conforme solicitação (Por Tipo)

# --- Área Expansível e Modular (Detalhes) ---
st.markdown("---")
st.subheader(f"Detalhamento das Transferências ({start_year} - {end_year})")

with st.expander("Ver Tabela Detalhada", expanded=False):
    if not df_map_data.empty:
        st.dataframe(
            df_map_data[['tx_nome_fantasia_osc', 'Tipo Jurídico', 'Qtd. Transferências', 'Valor Formatado', 'latitude', 'longitude']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("Sem dados para exibir.")

with st.expander("Análise Gráfica (Top 10 Beneficiárias)", expanded=True):
    if not df_map_data.empty:
        top_10 = df_map_data.nlargest(10, 'Valor Total Recebido')
        fig = px.bar(
            top_10,
            x='Valor Total Recebido',
            y='tx_nome_fantasia_osc',
            orientation='h',
            title=f"Gráfico 1 - Top 10 Maiores Beneficiárias ({start_year}-{end_year})",
            text_auto='.2s'
        )
        fig = apply_academic_chart_style(fig)
        # Fix y axis order
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Sem dados para gráfico.")
