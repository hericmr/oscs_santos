import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add parent directory to path to allow importing utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard_utils.styles import apply_academic_style
from dashboard_utils.visualizations import apply_academic_chart_style
from dashboard_utils.data_loader import load_csv_robust

# Page Configuration
st.set_page_config(page_title="Correspondencia de Transferências", page_icon=None, layout="wide")

# Apply Styles
apply_academic_style()

# Title
st.markdown("<h1>Correspondência de Transferências e Recursos</h1>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align: justify;">
Esta página descreve o processo de vinculação entre os dados do Mapa das OSCs e os arquivos de prestação de contas da Prefeitura de Santos. 
Como o Mapa das OSCs não informa as transferências municipais, foi necessário cruzar as bases para completar o panorama.
Os dados abrangem transferências de 2016 a 2025.
<br><br>
No cruzamento, algumas transferências apareceram para entidades não encontradas no Mapa das OSCs, principalmente por divergências de cadastro ou ausência da organização na plataforma.
</p>
<hr>
""", unsafe_allow_html=True)

# Helper: Load Data
@st.cache_data
def load_matching_data():
    base_path = os.path.join(os.path.dirname(__file__), '../data')
    
    # Files
    file_summary = os.path.join(base_path, 'tabela_resumo_recursos_por_osc.csv')
    file_complete = os.path.join(base_path, 'tabela_recursos_osc_match_completo.csv')
    file_unmatched = os.path.join(base_path, 'relatorio_nomes_nao_correspondidos.csv')
    
    # Load
    try:
        df_summary = load_csv_robust(file_summary)
        df_complete = load_csv_robust(file_complete)
        df_unmatched = load_csv_robust(file_unmatched)
        
        # Ensure match_type is string and fill NaNs
        if 'match_type' in df_complete.columns:
            df_complete['match_type'] = df_complete['match_type'].fillna('None').astype(str)
            
    except FileNotFoundError:
        st.error(f"Arquivos de dados não encontrados em {base_path}. Verifique se a etapa de matching foi executada.")
        return None, None, None
        
    return df_summary, df_complete, df_unmatched

df_summary, df_complete, df_unmatched = load_matching_data()

if df_complete is not None:

    # --- Global Filters ---
    st.markdown("### Filtros Globais")
    
    # Year Filter
    all_years = sorted([y for y in df_complete['ano_recurso'].unique() if pd.notna(y)])
    selected_years = st.multiselect("Selecione o(s) Ano(s):", all_years, default=all_years)
    
    if not selected_years:
        st.warning("Selecione pelo menos um ano para visualizar os dados.")
        st.stop()
        
    # Apply Filter to Main Dataframe
    df_filtered = df_complete[df_complete['ano_recurso'].isin(selected_years)].copy()
    
    # --- KPIs ---
    # Recalculate based on FILTERED data
    total_repassado_mapeado = df_filtered[df_filtered['match_type'] != 'None']['valor_repasse'].sum()
    total_repassado_geral = df_filtered['valor_repasse'].sum()
    
    # Calculate unmatched from filtered data
    df_filtered_unmatched = df_filtered[df_filtered['match_type'] == 'None']
    total_repassado_nao_mapeado = df_filtered_unmatched['valor_repasse'].sum()
    
    pct_cobertura = (total_repassado_mapeado / total_repassado_geral) * 100 if total_repassado_geral > 0 else 0
    
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric("Total Mapeado (OSCs Identificadas)", f"R$ {total_repassado_mapeado:,.2f}")
    with kpi2:
        st.metric("Total Não Identificado", f"R$ {total_repassado_nao_mapeado:,.2f}")
    with kpi3:
        st.metric("Cobertura do Valor Total", f"{pct_cobertura:.1f}%")
        
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs(["Visão por OSC (Ano a Ano)", "Auditoria de Match", "Não Correspondidos"])
    
    # --- TAB 1: Visão por OSC ---
    with tab1:
        st.markdown("### Ranking e Evolução de Recursos por OSC")
        
        # Prepare Data: Pivot by Year
        # Filter only matched from the already time-filtered dataset
        df_matched = df_filtered[df_filtered['match_type'] != 'None'].copy()
        
        # Ensure natureza exists
        if 'natureza_juridica_desc' not in df_matched.columns:
             df_matched['natureza_juridica_desc'] = 'N/A'
        else:
             df_matched['natureza_juridica_desc'] = df_matched['natureza_juridica_desc'].fillna('N/A')

        # Nature Filter (Specific to this view)
        all_natures = df_matched['natureza_juridica_desc'].unique()
        selected_nature = st.multiselect("Filtrar por Natureza Jurídica:", all_natures, default=all_natures)
        
        if selected_nature:
            df_matched = df_matched[df_matched['natureza_juridica_desc'].isin(selected_nature)]
            
        # Pivot Table
        # We pivot on the filtered data, so columns will only be the selected years
        pivot_df = df_matched.pivot_table(
            index=['match_name', 'match_cnpj', 'natureza_juridica_desc'],
            columns='ano_recurso',
            values='valor_repasse',
            aggfunc='sum',
            fill_value=0
        ).reset_index()
        
        # Add Total Column
        # Identify year columns dynamically
        year_cols = [c for c in pivot_df.columns if isinstance(c, (int, float)) or (isinstance(c, str) and c.isdigit())]
        pivot_df['Total'] = pivot_df[year_cols].sum(axis=1)
        
        # Sort
        pivot_df = pivot_df.sort_values('Total', ascending=False)
        
        # Formatting for display
        format_dict = {col: 'R$ {:,.2f}' for col in year_cols + ['Total']}
        
        # Display Table
        st.dataframe(
            pivot_df.style.format(format_dict),
            use_container_width=True,
            column_config={
                "match_name": "Nome da OSC (Oficial)",
                "match_cnpj": "CNPJ",
                "natureza_juridica_desc": "Natureza Jurídica",
                "Total": "Valor Total Recebido"
            },
            hide_index=True
        )
        
        # Chart: Top 15 (Total of Selection)
        if not pivot_df.empty:
            top_15 = pivot_df.head(15).sort_values('Total', ascending=True)
            fig_bar = px.bar(
                top_15,
                x='Total',
                y='match_name',
                orientation='h',
                title='Top 15 OSCs por Volume de Recursos (Total do Período Selecionado)',
                text_auto='.2s',
                labels={'Total': 'Total Recebido (R$)', 'match_name': 'OSC'}
            )
            fig_bar.update_layout(xaxis_title="Valor (R$)", yaxis_title="")
            fig_bar.update_traces(marker_color='#333333')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Nenhum dado encontrado para os filtros selecionados.")

    # --- TAB 2: Auditoria ---
    with tab2:
        st.markdown("### Detalhes da Correspondência (Auditoria)")
        st.markdown(f"Mostrando lançamentos para os anos: {', '.join(map(str, selected_years))}")
        
        # We already filtered by year globally, so just filter by Match Type
        match_types = df_filtered['match_type'].unique()
        selected_types = st.multiselect("Tipo de Match:", match_types, default=[t for t in match_types if t != 'None'])
            
        # Filter Data
        audit_df = df_filtered[df_filtered['match_type'].isin(selected_types)]
        
        st.dataframe(
            audit_df[['beneficiaria_nome', 'match_name', 'match_cnpj', 'match_type', 'score', 'valor_repasse', 'ano_recurso']],
            use_container_width=True,
            column_config={
                "beneficiaria_nome": "Beneficiário (Original)",
                "match_name": "OSC Vinculada",
                "match_type": "Tipo de Match",
                "score": "Score Similaridade",
                "valor_repasse": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
                "ano_recurso": st.column_config.NumberColumn("Ano", format="%d")
            }
        )
        
        st.info("**Tipos de Match:**\n* **Exact**: Nome idêntico (normalizado).\n* **Substring**: Nome contido no outro.\n* **Fuzzy**: Similaridade ortográfica alta.\n* **Manual**: Regra de negócio específica.")

    # --- TAB 3: Não Correspondidos ---
    with tab3:
        st.markdown("### Beneficiários Não Encontrados no Cadastro")
        st.markdown(f"Listando entidades não identificadas nos anos: {', '.join(map(str, selected_years))}")
        
        # Use df_filtered_unmatched derived from the global filter
        # Aggregate by name since we might have multiple entries per year or across years
        unmatched_summary = df_filtered_unmatched.groupby(['beneficiaria_nome', 'beneficiaria_nome_norm'])['valor_repasse'].sum().reset_index()
        
        st.dataframe(
            unmatched_summary.sort_values('valor_repasse', ascending=False),
            use_container_width=True,
            column_config={
                "beneficiaria_nome": "Nome no Recurso",
                "beneficiaria_nome_norm": "Nome Normalizado",
                "valor_repasse": st.column_config.NumberColumn("Valor Total", format="R$ %.2f")
            }
        )
        
        st.warning("Nota: Muitos itens nesta lista podem ser empresas privadas, APMs ou entidades de fora de Santos.")

else:
    st.info("Aguardando carregamento dos dados...")
