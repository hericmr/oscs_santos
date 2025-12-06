import streamlit as st
import pandas as pd

def render_key_results(df):
    """
    Renders the 'Principais Resultados' section with key metrics.
    Display: "Do total de [Active] OSCs em atividade em Santos, [OS] OSs e [OSCIP] são OSCIPs."
    """
    
    # Ensure necessary columns exist
    if 'situacao_cadastral' not in df.columns or 'cd_natureza_juridica_osc' not in df.columns:
        st.warning("Dados incompletos para gerar os Principais Resultados.")
        return

    # Filter for ACTIVE OSCs
    active_df = df[df['situacao_cadastral'] == 'Ativa']
    total_active = len(active_df)

    # Calculate OS (Natureza Jurídica 3301)
    # 3301 = Organização Social (Civil) -> Actually 330-1 is Organização Social.
    # Note: Using 3301 based on internal project convention seen in legacy code.
    os_count = len(active_df[active_df['cd_natureza_juridica_osc'] == 3301])

    # Calculate OSCIP 
    # Logic: Any Active OSC that is NOT an OS (3301) is considered OSCIP for this specific text metric.
    # This is a simplification requested by the user ("7xxxx são OSCIPs" vs "xxxx OSs").
    oscip_count = len(active_df[active_df['cd_natureza_juridica_osc'] != 3301])

    # Styling for the container
    st.markdown("### Principais Resultados")
    
    # Create a styled box
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
                Do total de <b>{total_active}</b> OSCs em atividade em Santos, 
                <b>{os_count}</b> são Organizações Sociais (OSs) e 
                <b>{oscip_count}</b> são classificadas como OSCIPs.
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
