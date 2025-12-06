import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.data_loader import load_data

st.set_page_config(page_title="Tendências", layout="wide")
from utils.styles import apply_academic_style
apply_academic_style()

st.title("Criação de Organizações da Sociedade Civil em Santos (1933–2025)")

# Custom CSS to reduce metric font size
st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

df = load_data()

if not df.empty and 'Ano_Fundacao' in df.columns:
    
    # Filter valid years
    df = df.dropna(subset=['Ano_Fundacao'])
    df['Ano_Fundacao'] = df['Ano_Fundacao'].astype(int)
    
    # Range Slider
    min_year = int(df['Ano_Fundacao'].min())
    max_year = int(df['Ano_Fundacao'].max())
    
    # st.subheader("Evolução da Criação de OSCs")
    
    col_filter, col_metrics = st.columns([1, 2])
    
    with col_filter:
        selected_range = st.slider("Selecione o período:", min_year, max_year, (1930, max_year))
    
    df_filtered = df[(df['Ano_Fundacao'] >= selected_range[0]) & (df['Ano_Fundacao'] <= selected_range[1])]
    
    # --- Detailed Matplotlib Chart ---
    year_counts = df_filtered['Ano_Fundacao'].value_counts().sort_index()

    if not year_counts.empty:
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # 1. Main line
        ax.plot(year_counts.index, year_counts.values,
                 marker='o', linestyle='-', linewidth=2.5, markersize=8,
                 label='Novas OSCs', color='#1f77b4', zorder=3)
        
        # 2. Dictatorship Band (1964-1985)
        # Only show if the selected range overlaps with the period
        dictatorship_start = 1964
        dictatorship_end = 1985
        
        if selected_range[0] <= dictatorship_end and selected_range[1] >= dictatorship_start:
            ax.axvspan(dictatorship_start, dictatorship_end, color='#d3d3d3', alpha=0.2,
                        label='Ditadura Militar (1964–1985)', zorder=1)
            
            # Label position
            label_x = (max(selected_range[0], dictatorship_start) + min(selected_range[1], dictatorship_end)) / 2
            label_y = year_counts.max() * 0.9
            
            ax.text(label_x, label_y,
                     'Ditadura Empresarial-Militar\n(1964–1985)',
                     ha='center', va='top', fontsize=10, color='gray', zorder=2)

        # 3. Legal Milestones
        milestones = {
            1938: ('Criação\ndo CNSS', '#d62728'),
            1998: ('Lei das\nOrganizações\nSociais', '#2ca02c'),
            1999: ('Lei das\nOSCIPs', '#ff7f0e'),
            2014: ('MROSC', '#9467bd'),
            2016: ('Decreto\ndo MROSC', '#8c564b')
        }
        
        # Base y position for labels (below x-axis)
        y_base = - (year_counts.max() * 0.05) if year_counts.max() > 0 else -1
        
        # Stagger offsets
        offsets = {
            1938: 1.0,
            1998: 1.0,
            1999: 2.5, 
            2014: 1.0,
            2016: 2.5
        }
        
        for year, (label, color) in milestones.items():
            if selected_range[0] <= year <= selected_range[1]:
                ax.axvline(x=year, color=color, linestyle='-', linewidth=2, alpha=0.9, zorder=2)
                
                text_y = y_base * offsets.get(year, 1.0)
                
                ax.text(year + 0.5, text_y,
                         f"{year} — {label}",
                         ha='left', va='top', fontsize=9, color=color,
                         fontweight='bold')
        
        # Axis and Grid
        ax.set_xlabel('Ano de Fundação', fontsize=12)
        ax.set_ylabel('Novas OSCs', fontsize=12)
        ax.set_title(f'Evolução Histórica da Criação de OSCs em Santos ({selected_range[0]} - {selected_range[1]})', fontsize=14, pad=20)
        ax.grid(True, linestyle=':', alpha=0.4)
        
        # Limits adjustment
        ax.set_ylim(bottom=y_base * 3.5)
        
        # Legend
        handles, labels_ = ax.get_legend_handles_labels()
        wanted = ['Novas OSCs', 'Ditadura Militar (1964–1985)']
        final_handles = [h for h, l in zip(handles, labels_) if l in wanted]
        final_labels = [l for l in labels_ if l in wanted]
        ax.legend(final_handles, final_labels, loc='upper left', fontsize='medium', frameon=True)
        
        st.pyplot(fig)
        
        # --- Statistics Section ---
        with col_metrics:
            st.markdown("### Resumo Estatístico")
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric("Total no Período", len(df_filtered))
            with m_col2:
                st.metric("Ano Pioneiro", df_filtered['Ano_Fundacao'].min())
            with m_col3:
                st.metric("Média Anual", f"{year_counts.mean():.1f}")

        st.markdown("---")
        st.subheader("Dados Detalhados do Período")
        
        # Calculate height: 35px per row + 38px buffer for header/borders
        # We limit to a sensible max (e.g. 1500px) to prevent browser canvas crashes (InvalidStateError)
        # caused by excessively large heights (>32k pixels).
        height_px = min((len(df_filtered) + 1) * 35 + 3, 1500)
        
        st.dataframe(df_filtered, use_container_width=True, height=height_px)
        
    else:
        st.info("Nenhuma OSC encontrada no período selecionado.")

else:
    st.error("Dados de data de fundação indisponíveis.")
