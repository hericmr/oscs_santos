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
    
    # --- Load Resource Data for All Years Analysis ---
    res_path = os.path.join(os.path.dirname(__file__), '../data/tabela_recursos_osc_match_completo.csv')
    
    analysis_html = ""
    
    if os.path.exists(res_path):
        try:
            df_res = pd.read_csv(res_path, sep=';', decimal=',')
            
            # Ensure proper types
            df_res['valor_repasse'] = pd.to_numeric(df_res['valor_repasse'], errors='coerce').fillna(0)
            
            # Get valid years sorted descending
            unique_years = sorted([y for y in df_res['ano_recurso'].dropna().unique()], reverse=True)
            unique_years = [int(y) for y in unique_years] # ensure integers
            
            analysis_parts = []
            
            for year in unique_years:
                # Filter Year and Matched
                df_year = df_res[(df_res['ano_recurso'] == year) & (df_res['match_type'] != 'None')]
                
                if df_year.empty:
                    continue
                
                # Check nature
                is_os = df_year['natureza_juridica_desc'] == 'Organizacao Social (OS)'
                
                # Stats for OS
                os_data = df_year[is_os]
                qtd_os = os_data['match_cnpj'].nunique()
                val_os = os_data['valor_repasse'].sum()
                
                # Stats for OSCIPs (Others)
                oscip_data = df_year[~is_os]
                qtd_oscip = oscip_data['match_cnpj'].nunique()
                val_oscip = oscip_data['valor_repasse'].sum()
                
                # Format HTML for this year
                year_block = f"""
<div style="margin-top: 15px; border-top: 1px solid #e0e0e0; padding-top: 10px;">
    <p style="margin-bottom: 5px; color: #555;"><strong>Análise de Repasses ({year}):</strong></p>
    <p style="margin-bottom: 5px;">
    Das <b>{oscip_count}</b> OSCIPs ativas, <b>{qtd_oscip}</b> receberam 
    <b>R$ {val_oscip:,.2f}</b>.
    </p>
    <p>
    Entre as <b>{os_count}</b> OSs ativas, <b>{qtd_os}</b> receberam 
    <b>R$ {val_os:,.2f}</b>.
    </p>
</div>
"""
                analysis_parts.append(year_block)
            
            analysis_html = "".join(analysis_parts)
            
        except Exception as e:
            print(f"Error calculating stats: {e}")
            analysis_html = f"<p style='color:red'>Erro ao carregar análise temporal: {e}</p>"

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
            <p style="font-size: 1.1rem; margin: 0; line-height: 1.6;">
                {summary_text}
            </p>
            {analysis_html}
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
