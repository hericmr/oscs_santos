import streamlit as st
from utils.data_loader import load_data
from utils.visualizations import plot_bar_chart, plot_heatmap

st.set_page_config(page_title="Áreas de Atuação", layout="wide")
from utils.styles import apply_academic_style
apply_academic_style()

st.title("Áreas de Atuação")

df = load_data()

if not df.empty and 'Area_Atuacao' in df.columns:
    # 1. Gráfico Geral das Áreas
    st.subheader("Distribuição por Área de Atuação Principal")
    
    # Contagem
    # area_counts = df['Area_Atuacao'].value_counts()
    # st.bar_chart(area_counts) 
    
    # Vamos usar nosso plotly para ser consistente
    fig_area = plot_bar_chart(df, 'Area_Atuacao', title="Contagem de OSCs por Área", orientation='v')
    fig_area.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_area, use_container_width=True)

    st.divider()

    # 2. Drilldown - Subáreas
    st.subheader("Detalhamento por Subárea")
    
    selected_area = st.selectbox("Selecione uma Área para ver detalhes:", df['Area_Atuacao'].unique())
    
    if selected_area:
        df_filtered = df[df['Area_Atuacao'] == selected_area]
        
        # Encontrar colunas de SubArea que tem valor 1.0
        # Colunas comeca com 'SubArea_'
        subarea_cols = [c for c in df.columns if c.startswith('SubArea_')]
        
        active_subareas = []
        for idx, row in df_filtered.iterrows():
            for c in subarea_cols:
                if row[c] == 1.0:
                    name = c.replace('SubArea_', '').replace('_', ' ')
                    active_subareas.append(name)
        
        if active_subareas:
            import pandas as pd
            df_sub = pd.DataFrame(active_subareas, columns=['SubArea'])
            fig_sub = plot_bar_chart(df_sub, 'SubArea', title=f"Subáreas em {selected_area}", orientation='v')
            # Ajustar altura se tiver muitas barras
            # fig_sub.update_layout(height=max(400, len(df_sub['SubArea'].unique()) * 20))
            st.plotly_chart(fig_sub, use_container_width=True)
        else:
            st.info("Nenhuma subárea específica identificada nestes registros.")

else:
    st.error("Dados de Área de Atuação indisponíveis.")
