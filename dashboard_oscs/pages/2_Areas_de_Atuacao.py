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

    # --- Tabela 5.1 (Adaptada) - Natureza Jurídica ---
    import pandas as pd
    
    st.markdown("### Tabela de Natureza Jurídica (Padrão IPEA)")

    if 'natureza_juridica_desc' in df.columns:
        # Calcular estatísticas
        total_geral = len(df)
        df_nat = df['natureza_juridica_desc'].value_counts().reset_index()
        df_nat.columns = ['Natureza Jurídica', 'Total de OSCs']
        
        # Calcular Porcentagens
        df_nat['(%) Em relação ao total'] = (df_nat['Total de OSCs'] / total_geral * 100).round(1)
        
        # Como não temos uma categoria "pai" hierárquica clara nos dados planos (ex: AssociaçãoPrivada vs AssociaçãoPublica),
        # assumiremos que cada linha é um grupo em si, então % do grupo é 100% ou deixamos vazio.
        # Seguindo a instrução "mantenha 100% ou deixe em branco" caso não haja subcategorias.
        df_nat['(%) Em relação ao grupo'] = "100.0"

        # Adicionar linha de Total
        row_total = pd.DataFrame({
            'Natureza Jurídica': ['<b>Total Geral</b>'],
            'Total de OSCs': [total_geral],
            '(%) Em relação ao total': [100.0],
            '(%) Em relação ao grupo': ['-']
        })
        
        df_display = pd.concat([df_nat, row_total], ignore_index=True)

        # Formatação de milhares
        df_display['Total de OSCs'] = df_display['Total de OSCs'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
        df_display['(%) Em relação ao total'] = df_display['(%) Em relação ao total'].astype(str)
        
        # HTML Styling para "Padrão Acadêmico/IPEA"
        # Usando HTML simples para controlar bordas e negrito
        html = df_display.to_html(index=False, escape=False, classes='ipea-table')
        
        # Injetar CSS específico para essa tabela
        st.markdown("""
        <style>
            .ipea-table {
                width: 100%;
                border-collapse: collapse;
                font-family: 'Times New Roman', Times, serif;
                font-size: 14px;
                color: black;
            }
            .ipea-table th {
                border-top: 2px solid black;
                border-bottom: 2px solid black;
                text-align: left;
                padding: 8px;
                font-weight: bold;
            }
            .ipea-table td {
                border-bottom: 1px solid #ddd;
                padding: 8px;
            }
            .ipea-table tr:last-child td {
                border-bottom: 2px solid black;
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.write(html, unsafe_allow_html=True)
        st.caption("Fonte: Mapa das OSCs (IPEA). Elaboração própria.")
    else:
        st.warning("Coluna 'natureza_juridica_desc' não encontrada nos dados.")

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
