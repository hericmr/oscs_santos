import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.visualizations import plot_pie_chart, plot_bar_chart

st.set_page_config(page_title="Visão Geral", layout="wide")
from utils.styles import apply_academic_style
apply_academic_style()

st.title("Visão Geral")

# Load Data
df = load_data()

if df.empty:
    st.error("Erro ao carregar os dados. Verifique se o arquivo data/oscs_santos.csv existe.")
else:
    # --- Principais Resultados ---
    # --- Principais Resultados ---
    from utils.components import render_key_results, render_employment_stats
    render_key_results(df)
    # render_employment_stats(df) # Hidden due to missing RAIS data
        
    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    
    total_oscs = len(df)
    ativas = len(df[df['situacao_cadastral'] == 'Ativa'])
    
    # Total de OS (Organizações Sociais - Código 3301)
    total_os = len(df[df['cd_natureza_juridica_osc'] == 3301]) if 'cd_natureza_juridica_osc' in df.columns else 0

    # Inicializar estado da seleção se não existir
    if 'selected_metric' not in st.session_state:
        st.session_state['selected_metric'] = None

    # Botões para interação
    if col1.button("Ver Lista", key="btn_total"):
        st.session_state['selected_metric'] = 'total'
    col1.metric("Total de OSCs", total_oscs)
    
    if col2.button("Ver Lista", key="btn_ativas"):
        st.session_state['selected_metric'] = 'ativas'
    col2.metric("OSCs Ativas", ativas)

    if col3.button("Ver Lista", key="btn_os"):
        st.session_state['selected_metric'] = 'os'
    col3.metric("Total de OS", total_os)

    # Exibição Condicional da Tabela
    if st.session_state['selected_metric']:
        st.divider()
        st.subheader("Detalhamento da Métrica Selecionada")
        
        detail_df = pd.DataFrame()
        
        if st.session_state['selected_metric'] == 'total':
            st.info("Mostrando todas as OSCs.")
            detail_df = df
            
        elif st.session_state['selected_metric'] == 'ativas':
            st.info("Mostrando apenas OSCs com situação cadastral Ativa.")
            detail_df = df[df['situacao_cadastral'] == 'Ativa']
        
        elif st.session_state['selected_metric'] == 'os':
            st.info("Mostrando apenas Organizações Sociais (Código 3301).")
            if 'cd_natureza_juridica_osc' in df.columns:
                detail_df = df[df['cd_natureza_juridica_osc'] == 3301]
            else:
                detail_df = pd.DataFrame()

        # Display table with dynamic height
        if not detail_df.empty:
            height = min((len(detail_df) + 1) * 35 + 3, 600) # Capping at 600px to avoid massive pages
            st.dataframe(detail_df, use_container_width=True, height=height)
            
            if st.button("Fechar Lista"):
                st.session_state['selected_metric'] = None
                st.rerun()
        else:
            st.warning("Nenhum registro encontrado para esta métrica.")

    # --- Tabela 6.3 (IPEA) - Natureza Jurídica: Santos (Distribuição por Bairro) ---
    st.divider()
    st.markdown("### Tabela 6.3 - OSCs por natureza jurídica segundo o bairro (Distribuição %)")
    st.markdown("Esta seção apresenta dados sobre a natureza jurídica das Organizações da Sociedade Civil - OSCs. Foram usadas para calcular o total de OSCs da cidade de Santos as naturezas associações privadas, fundações privadas e organizações religiosas pessoas de direito privado sem fins lucrativos previstas no Código Civil – Lei n o 10.406/2002, bem como as organizações sociais assim qualificadas por Lei Federal, Estadual, Distrital ou Municipal.")
    
    # Função para extrair Bairro (Reutilizada de Mapa_Repasses)
    def extract_bairro(addr):
        if not isinstance(addr, str): return "Não Identificado"
        parts = addr.split(',')
        try:
            # Procurar 'Santos'
            sanitized_parts = [p.strip().upper() for p in parts]
            if 'SANTOS' in sanitized_parts:
                idx = sanitized_parts.index('SANTOS')
                if idx > 0:
                    possible_bairro = parts[idx-1].strip()
                    if len(possible_bairro) < 3 and idx > 1:
                         return parts[idx-2].strip()
                    return possible_bairro.title() # Capitalize
            if len(parts) >= 4:
                return parts[-3].strip().title()
        except:
            pass
        return "Não Identificado"

    if 'Bairro' not in df.columns and 'tx_endereco_completo' in df.columns:
        df['Bairro'] = df['tx_endereco_completo'].apply(extract_bairro)
        
    if 'Bairro' in df.columns and 'cd_natureza_juridica_osc' in df.columns:
        # Filter out invalid neighborhoods if needed, or keep all
        df_bairro = df.copy()
        
        # Mapping Names
        nat_jur_labels = {
            3999: "Associação Privada",
            3069: "Fundação Privada",
            3220: "Org. Religiosa",
            3301: "Org. Social (OS)"
        }
        df_bairro['Natureza_Label'] = df_bairro['cd_natureza_juridica_osc'].map(nat_jur_labels).fillna("Outros")
        
        # Pivot Table: Index=Bairro, Columns=Natureza, Values=Count
        pivot = pd.crosstab(df_bairro['Bairro'], df_bairro['Natureza_Label'], margins=True, margins_name="Total")
        
        # Calculate Percentages Row-wise
        pivot_pct = pivot.div(pivot['Total'], axis=0).mul(100)
        
        # Format as String with %
        for col in pivot_pct.columns:
            pivot_pct[col] = pivot_pct[col].apply(lambda x: f"{x:.1f}%")
            
        # Reset Index to make Bairro a column
        pivot_display = pivot_pct.reset_index()
        
        # Filter out random/bad extractions if list is too long (Optional, but good for UX)
        # For now, sorting by Total Count (descending) to show most relevant neighborhoods first
        # We need the original counts to sort
        pivot_counts = pivot.reset_index()
        valid_bairros = pivot_counts.sort_values('Total', ascending=False)['Bairro'].tolist()
        
        # Remove 'Total' row from sorting and put it at the end or top
        if 'Total' in valid_bairros:
            valid_bairros.remove('Total')
            valid_bairros = ['Total'] + valid_bairros # Total first
            
        # Reorder DataFrame
        pivot_display['Bairro'] = pd.Categorical(pivot_display['Bairro'], categories=valid_bairros, ordered=True)
        pivot_display = pivot_display.sort_values('Bairro')
        
        # Rename Index Column for display
        pivot_display = pivot_display.rename(columns={'Bairro': 'Bairro / Localidade'})

        # Exibir Tabela
        st.dataframe(pivot_display, use_container_width=True, hide_index=True)
        st.caption("Fonte: Mapa das OSCs (Recorte Santos) - Bairros inferidos do endereço.")
    else:
        st.warning("Dados de endereço insuficientes para extrair bairros.")

    st.divider()

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
                2305: "Empresa Individual de Resp. Limitada (Natureza Empresária)",
                2313: "Empresa Individual de Resp. Limitada (Natureza Simples)"
            }
            
            # Create a new column with mapped values, keeping original if not found
            df['Natureza_Juridica_Desc'] = df['cd_natureza_juridica_osc'].map(nat_jur_mapping).fillna(df['cd_natureza_juridica_osc'])
            
            fig_pie = plot_pie_chart(df, 'Natureza_Juridica_Desc', title="Distribuição por Natureza Jurídica")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Coluna de Natureza Jurídica não encontrada.")

    with c2:
        # st.subheader("OSCs por Ano de Fundação (Top 20)")
        if 'Ano_Fundacao' in df.columns:
            # Filtrar anos válidos
            df_year = df.dropna(subset=['Ano_Fundacao'])
            counts = df_year['Ano_Fundacao'].astype(int).value_counts().sort_index()
            # Plotar linha ou barra? Barra é melhor para distribuição discreta.
            # Vou plotar os ultimos 50 anos ou tudo?
            fig_bar = plot_bar_chart(df_year, 'Ano_Fundacao', title="Distribuição por Ano de Fundação", orientation='v')
            st.plotly_chart(fig_bar, use_container_width=True)
