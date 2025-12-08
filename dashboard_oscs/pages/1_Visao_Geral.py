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
    st.markdown("### Tabela 6.3 - Distribuição de OSCs por Bairro e Natureza Jurídica")

    # 1. Função de Extração Melhorada
    def extract_bairro_safe(addr):
        if not isinstance(addr, str): return "Não Identificado"
        parts = [p.strip() for p in addr.split(',')]
        
        # Tenta achar 'Santos' e pegar o anterior
        for i, part in enumerate(parts):
            if 'SANTOS' in part.upper():
                if i > 0:
                    candidate = parts[i-1]
                    # Validação básica: Bairro não costuma ser número ou muito curto
                    if not candidate.isdigit() and len(candidate) > 2:
                        return candidate.title()
        
        # Fallback: pega o penúltimo se houver partes suficientes
        if len(parts) >= 3:
             candidate = parts[-2] if 'CEP' not in parts[-1] else parts[-3]
             if not candidate.isdigit() and len(candidate) > 2:
                 return candidate.title()
                 
        return "Não Identificado"

    if 'tx_endereco_completo' in df.columns:
        # Criar coluna de bairro se não existir
        if 'Bairro' not in df.columns:
            df['Bairro'] = df['tx_endereco_completo'].apply(extract_bairro_safe)

        # 2. Filtragem e Tratamento (Pareto: Focar nos bairros relevantes)
        df_display = df.copy()
        
        # Mapeamento das Naturezas (Simplificando nomes longos)
        nat_jur_labels = {
            3999: "Associação",
            3069: "Fundação",
            3220: "Religiosa",
            3301: "OS (Social)"
        }
        df_display['Natureza'] = df_display['cd_natureza_juridica_osc'].map(nat_jur_labels).fillna("Outros")

        # Agrupar bairros pequenos em "Outros" (ex: menos de 5 OSCs)
        bairro_counts = df_display['Bairro'].value_counts()
        cutoff = 5 # Bairros com menos de X OSCs viram "Outros"
        main_bairros = bairro_counts[bairro_counts >= cutoff].index
        df_display['Bairro_Clean'] = df_display['Bairro'].apply(lambda x: x if x in main_bairros else 'Outros / Pequenos')

        # 3. Controles de Visualização
        col_opt1, col_opt2 = st.columns([1, 3])
        view_mode = col_opt1.radio("Visualizar dados em:", ["Porcentagem (%)", "Quantidade (N)", "Ambos"], horizontal=True)

        # 4. Criando a Pivot Table
        if view_mode == "Quantidade (N)":
            pivot = pd.crosstab(df_display['Bairro_Clean'], df_display['Natureza'], margins=True, margins_name="Total")
            # Ordenar por Total
            pivot = pivot.sort_values('Total', ascending=False)
            
            # Styling: Heatmap simples nos números
            st.dataframe(
                pivot.style.background_gradient(cmap="Blues", subset=pivot.columns.drop("Total", errors='ignore')),
                use_container_width=True,
                height=500
            )

        elif view_mode == "Porcentagem (%)":
            # Crosstab normalizado pela linha (index) -> Soma da linha = 100%
            pivot = pd.crosstab(df_display['Bairro_Clean'], df_display['Natureza'], normalize='index').mul(100)
            
            # Adicionar coluna de Contagem Total para ordenação
            total_counts = df_display['Bairro_Clean'].value_counts()
            pivot['Total (N)'] = total_counts
            
            # Ordenar e remover coluna auxiliar se não quiser mostrar
            pivot = pivot.sort_values('Total (N)', ascending=False)
            
            # Formatação bonita com Pandas Styler
            st.dataframe(
                pivot.style.format("{:.1f}%", subset=pivot.columns.drop('Total (N)'))
                     .background_gradient(cmap="Greens", axis=None, subset=pivot.columns.drop('Total (N)')), # Axis=None aplica gradiente na tabela toda
                use_container_width=True,
                height=500
            )

        else: # "Ambos" (Lógica original melhorada)
            pivot_count = pd.crosstab(df_display['Bairro_Clean'], df_display['Natureza'], margins=True, margins_name="Total")
            pivot_pct = pd.crosstab(df_display['Bairro_Clean'], df_display['Natureza'], normalize='index').mul(100)
            
            # Construir tabela combinada manualmente para garantir ordem
            combined = pd.DataFrame(index=pivot_count.index.sort_values()) # Index alfabético ou poderia ordenar por volume
            
            # Ordenar bairros por volume total antes de iterar
            order_idx = pivot_count.sort_values('Total', ascending=False).index
            combined = combined.reindex(order_idx)

            cols = sorted([c for c in pivot_count.columns if c != 'Total']) + ['Total']
            
            for col in cols:
                combined[f"{col} (N)"] = pivot_count[col]
                if col != 'Total': # Não faz sentido % do Total geral na linha, pois é sempre 100%
                    combined[f"{col} (%)"] = pivot_pct[col].apply(lambda x: f"{x:.1f}%")

            st.dataframe(combined, use_container_width=True, height=600)

        st.caption(f"Nota: Bairros com menos de {cutoff} OSCs foram agrupados em 'Outros / Pequenos' para facilitar a visualização.")

    else:
        st.warning("Coluna de endereço não disponível para gerar esta tabela.")

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
