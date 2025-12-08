import streamlit as st
import pandas as pd

def render_key_results(df):
    """
    Renders the 'Principais Resultados' section with key metrics.
    Display: "Do total de [Active] OSCs em atividade em Santos, [OS] OSs e [OSCIP] são OSCIPs."
    Now expandable with 2025 Resource Analysis.
    """
    import os
    
    # Ensure necessary columns exist
    if 'situacao_cadastral' not in df.columns or 'cd_natureza_juridica_osc' not in df.columns:
        st.warning("Dados incompletos para gerar os Principais Resultados.")
        return

    # Filter for ACTIVE OSCs
    active_df = df[df['situacao_cadastral'] == 'Ativa']
    total_active = len(active_df)

    # Calculate OS (Natureza Jurídica 3301)
    os_count = len(active_df[active_df['cd_natureza_juridica_osc'] == 3301])

    # Calculate OSCIP (Non-OS simplification)
    oscip_count = len(active_df[active_df['cd_natureza_juridica_osc'] != 3301])
    


    # Styling for the container
    st.markdown("### Principais Resultados")
    
    # Text Label (Original Summary)
    summary_text = f"Do total de <b>{total_active}</b> OSCs em atividade em Santos, <b>{os_count}</b> são Organizações Sociais (OSs) e <b>{oscip_count}</b> são classificadas como OSCIPs."
    
    # Create a styled box (Static, Simple, Scrollable if too long? No, user asks for simple presentation, just list them)
    # We might want to limit height if it's huge, but let's just list them for now as requested.
    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa;
            border-left: 5px solid #333333;
            padding: 1.5rem;
            border-radius: 5px;
            font-family: 'Arial', sans-serif;
            color: #000000;
            margin-bottom: 2rem;
        ">
                {summary_text}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_employment_stats(df):
    """
    Renders employment statistics (Vínculos Empregatícios).
    """
    st.markdown("### Vínculos Empregatícios")
    
    # Identify employment column - trying common variations
    emp_col = None
    for col in ['nr_trabalhadores', 'nr_trabalhadores_vinculo', 'qtd_vinc_ativos', 'rais']:
        if col in df.columns:
            emp_col = col
            break
            
    if emp_col is None:
        st.warning("⚠️ Dados de vínculos empregatícios não encontrados (Colunas esperadas: 'nr_trabalhadores' ou similar). Exibindo valores zerados.")
        # Create dummy column for calculation to prevent crash, but values are 0
        df_calc = df.copy()
        df_calc['nr_trabalhadores'] = 0
        emp_col = 'nr_trabalhadores'
    else:
        df_calc = df
    
    # Filter Active
    if 'situacao_cadastral' in df_calc.columns:
        active_df = df_calc[df_calc['situacao_cadastral'] == 'Ativa']
    else:
        active_df = df_calc

    # 1. OS Stats
    os_df = active_df[active_df['cd_natureza_juridica_osc'] == 3301]
    total_os = len(os_df)
    
    # WinthOUT links (== 0 or NaN)
    os_no_link = len(os_df[(os_df[emp_col] == 0) | (os_df[emp_col].isna())])
    pct_os_no_link = (os_no_link / total_os * 100) if total_os > 0 else 0
    
    # With links
    os_with_link = os_df[os_df[emp_col] > 0]
    total_links_os = int(os_with_link[emp_col].sum())
    avg_links_os = (total_links_os / total_os) if total_os > 0 else 0

    # 2. OSCIP Stats (Non-OS)
    oscip_df = active_df[active_df['cd_natureza_juridica_osc'] != 3301]
    total_oscip = len(oscip_df)
    
    # Without links
    oscip_no_link = len(oscip_df[(oscip_df[emp_col] == 0) | (oscip_df[emp_col].isna())])
    pct_oscip_no_link = (oscip_no_link / total_oscip * 100) if total_oscip > 0 else 0
    
    # With links
    oscip_with_link = oscip_df[oscip_df[emp_col] > 0]
    total_links_oscip = int(oscip_with_link[emp_col].sum())
    avg_links_oscip = (total_links_oscip / total_oscip) if total_oscip > 0 else 0

    # Render styled box
    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa;
            border-left: 5px solid #333333;
            padding: 1.5rem;
            border-radius: 5px;
            font-family: 'Arial', sans-serif;
            color: #000000;
            margin-bottom: 2rem;
        ">
            <p style="font-size: 1.1rem; margin: 0; line-height: 1.6;">
                <b>{pct_os_no_link:.1f}%</b> das OSs e <b>{pct_oscip_no_link:.1f}%</b> das OSCIPs não registram vínculos
                empregatícios formais. <br><br>
                Das que registram, as OSs têm <b>{total_links_os}</b> vínculos
                de trabalhos formais e as OSCIPs, <b>{total_links_oscip}</b>. <br>
                A média é <b>{avg_links_os:.1f}</b> vínculos por OS
                e <b>{avg_links_oscip:.1f}</b> por OSCIP.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_kpis_section(df):
    """
    Render KPIs and interactive lists for Overview page.
    """
    col1, col2, col3 = st.columns(3)
    
    total_oscs = len(df)
    ativas = len(df[df['situacao_cadastral'] == 'Ativa']) if 'situacao_cadastral' in df.columns else 0
    total_os = len(df[df['cd_natureza_juridica_osc'] == 3301]) if 'cd_natureza_juridica_osc' in df.columns else 0

    # Initialize session state for interactivity
    if 'selected_metric' not in st.session_state:
        st.session_state['selected_metric'] = None

    # KPI Buttons
    if col1.button("Ver Lista", key="btn_total"):
        st.session_state['selected_metric'] = 'total'
    col1.metric("Total de OSCs", total_oscs)
    
    if col2.button("Ver Lista", key="btn_ativas"):
        st.session_state['selected_metric'] = 'ativas'
    col2.metric("OSCs Ativas", ativas)

    if col3.button("Ver Lista", key="btn_os"):
        st.session_state['selected_metric'] = 'os'
    col3.metric("Total de OS", total_os)

    # Interactive Details Table
    if st.session_state['selected_metric']:
        st.divider()
        st.subheader("Detalhamento da Métrica Selecionada")
        
        detail_df = pd.DataFrame()
        
        if st.session_state['selected_metric'] == 'total':
            st.info("Mostrando todas as OSCs.")
            detail_df = df
            
        elif st.session_state['selected_metric'] == 'ativas':
            st.info("Mostrando apenas OSCs com situação cadastral Ativa.")
            detail_df = df[df['situacao_cadastral'] == 'Ativa'] if 'situacao_cadastral' in df.columns else df
        
        elif st.session_state['selected_metric'] == 'os':
            st.info("Mostrando apenas Organizações Sociais (Código 3301).")
            if 'cd_natureza_juridica_osc' in df.columns:
                detail_df = df[df['cd_natureza_juridica_osc'] == 3301]
        
        if not detail_df.empty:
            height = min((len(detail_df) + 1) * 35 + 3, 600)
            st.dataframe(detail_df, use_container_width=True, height=height)
            
            if st.button("Fechar Lista"):
                st.session_state['selected_metric'] = None
                st.rerun()
        else:
            st.warning("Nenhum registro encontrado.")
    
    st.divider()

def render_table_6_3(df):
    """
    Render Table 6.3 - OSCs by Legal Nature and Neighborhood.
    """
    st.markdown("Esta seção apresenta dados sobre a natureza jurídica das Organizações da Sociedade Civil - OSCs. Foram usadas para calcular o total de OSCs da cidade de Santos as naturezas associações privadas, fundações privadas e organizações religiosas pessoas de direito privado sem fins lucrativos previstas no Código Civil – Lei n o 10.406/2002, bem como as organizações sociais assim qualificadas por Lei Federal, Estadual, Distrital ou Municipal.")
    st.markdown("### Tabela 6.3 - OSCs por natureza jurídica segundo o bairro (Distribuição %)")
    
    from dashboard_utils.data_cleaning import extract_bairro
    
    # Apply extraction if column doesn't exist
    df_proc = df.copy()
    if 'Bairro' not in df_proc.columns and 'tx_endereco_completo' in df_proc.columns:
        df_proc['Bairro'] = df_proc['tx_endereco_completo'].apply(extract_bairro)
        
    if 'Bairro' in df_proc.columns and 'cd_natureza_juridica_osc' in df_proc.columns:
        nat_jur_labels = {
            3999: "Associação Privada",
            3069: "Fundação Privada",
            3220: "Org. Religiosa",
            3301: "Org. Social (OS)"
        }
        df_proc['Natureza_Label'] = df_proc['cd_natureza_juridica_osc'].map(nat_jur_labels).fillna("Outros")
        
        pivot = pd.crosstab(df_proc['Bairro'], df_proc['Natureza_Label'], margins=True, margins_name="Total")
        pivot_pct = pivot.div(pivot['Total'], axis=0).mul(100)
        
        for col in pivot_pct.columns:
            pivot_pct[col] = pivot_pct[col].apply(lambda x: f"{x:.1f}%")
            
        pivot_display = pivot_pct.reset_index()
        
        # Sort by Total Volume
        pivot_counts = pivot.reset_index()
        valid_bairros = pivot_counts.sort_values('Total', ascending=False)['Bairro'].tolist()
        if 'Total' in valid_bairros:
            valid_bairros.remove('Total')
            valid_bairros = ['Total'] + valid_bairros
            
        pivot_display['Bairro'] = pd.Categorical(pivot_display['Bairro'], categories=valid_bairros, ordered=True)
        pivot_display = pivot_display.sort_values('Bairro')
        pivot_display = pivot_display.rename(columns={'Bairro': 'Bairro / Localidade'})

        st.dataframe(pivot_display, use_container_width=True, hide_index=True)
        st.caption("Fonte: Mapa das OSCs (Recorte Santos) - Bairros inferidos do endereço.")
    else:
        st.warning("Dados insuficientes para gerar Tabela 6.3.")
        
    st.divider()
