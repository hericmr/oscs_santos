```python
import streamlit as st
from dashboard_utils.data_loader import load_data
from dashboard_utils.visualizations import plot_bar_chart, plot_pie_chart, apply_academic_chart_style
import pandas as pd

st.set_page_config(page_title="Áreas de Atuação", layout="wide")
from dashboard_utils.styles import apply_academic_style
apply_academic_style()

st.title("Áreas de Atuação")

df = load_data()

if not df.empty and 'Area_Atuacao' in df.columns:


    # --- Tabela: Áreas e Subáreas de Atuação (IPEA) ---
    # --- Tabela: Áreas e Subáreas de Atuação (IPEA) ---
    st.markdown("### Tabela 1 - Número de OSCs, segundo a finalidade de atuação")
    st.markdown("Esta seção trata sobre as áreas de atuação das Organizações da Sociedade Civil - OSCs.")

    # Lógica de Agregação Hierárquica
    # As colunas são binárias (One-Hot). 
    # Area_X = 1 -> OSC atua na Area X
    # SubArea_Y = 1 -> OSC atua na SubArea Y
    
    # Mapeamento hierárquico (Hardcoded baseado nas colunas do CSV para garantir estrutura)
    hierarchy = {
        'Assistência Social': ['SubArea_Assistencia_social'],
        'Cultura e Recreação': ['SubArea_Cultura_e_arte', 'SubArea_Esportes_e_recreacao'],
        'Desenvolvimento e Defesa de Direitos': ['SubArea_Desenvolvimento_e_defesa_de_direitos', 'SubArea_Associacoes_de_atividades_nao_especificadas_anteriormente'],
        'Educação e Pesquisa': ['SubArea_Educacao_infantil', 'SubArea_Ensino_fundamental', 'SubArea_Ensino_superior', 'SubArea_Educacao_profissional', 'SubArea_Atividades_de_apoio_a_educacao', 'SubArea_Outras_formas_de_educacao_ensino', 'SubArea_Estudos_e_pesquisas'],
        'Saúde': ['SubArea_Hospitais', 'SubArea_Outros_servicos_de_saude'],
        'Religião': ['SubArea_Religiao'],
        'Associações Patronais e Profissionais': ['SubArea_Associacoes_empresariais_e_patronais', 'SubArea_Associacoes_profissionais'],
        'Outras Atividades Associativas': []
    }

    # Mapa de colunas Area_ para nomes legíveis (deve bater com keys do hierarchy)
    area_col_map = {
        'Area_Assistencia_social': 'Assistência Social',
        'Area_Cultura_e_recreacao': 'Cultura e Recreação',
        'Area_Desenvolvimento_e_defesa_de_direitos_e_interesses': 'Desenvolvimento e Defesa de Direitos',
        'Area_Educacao_e_pesquisa': 'Educação e Pesquisa',
        'Area_Saude': 'Saúde',
        'Area_Religiao': 'Religião',
        'Area_Associacoes_patronais_e_profissionais': 'Associações Patronais e Profissionais',
        'Area_Outras_atividades_associativas': 'Outras Atividades Associativas'
    }

    table_rows = []
    total_oscs = len(df)

    # Iterar sobre as Áreas Principais
    for area_col, area_name in area_col_map.items():
        if area_col in df.columns:
            # Calcular Total da Área
            count_area = df[area_col].sum()
            if count_area == 0: continue # Skip areas with 0 results

            try:
                pct_total_area = (count_area / total_oscs) * 100
            except: 
                pct_total_area = 0

            # Adicionar Linha da Categoria Principal
            table_rows.append({
                'Area': f"<b>{area_name}</b>",
                'Total': count_area,
                'Perc_Total': pct_total_area,
                'Perc_Group': None # Categoria principal não tem % grupo
            })

            # Processar Subáreas
            subareas = hierarchy.get(area_name, [])
            for sub_col in subareas:
                if sub_col in df.columns:
                    count_sub = df[df[area_col] == 1][sub_col].sum() # Contar subarea APENAS dentro da area pai, embora dados devam ser consistentes
                    
                    if count_sub > 0:
                        try:
                            pct_total_sub = (count_sub / total_oscs) * 100
                            pct_group_sub = (count_sub / count_area) * 100
                        except:
                            pct_total_sub = 0
                            pct_group_sub = 0
                            
                        # Limpar nome da subarea
                        sub_name = sub_col.replace('SubArea_', '').replace('_', ' ').capitalize()
                        
                        table_rows.append({
                            'Area': f"<span style='padding-left: 20px;'>{sub_name}</span>",
                            'Total': count_sub,
                            'Perc_Total': pct_total_sub,
                            'Perc_Group': pct_group_sub
                        })

    # Adicionar Total Geral
    table_rows.append({
        'Area': "<b>Total Geral de OSCs</b>",
        'Total': total_oscs,
        'Perc_Total': 100.0,
        'Perc_Group': None
    })

    # Criar DataFrame final
    df_area_table = pd.DataFrame(table_rows)

    # Formatação Final
    df_area_table['Total de OSCs'] = df_area_table['Total'].apply(lambda x: f"{int(x):,.0f}".replace(",", "."))
    df_area_table['(%) Em relação ao total'] = df_area_table['Perc_Total'].apply(lambda x: f"{x:.1f}")
    df_area_table['(%) Em relação ao grupo'] = df_area_table['Perc_Group'].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "-")

    # Selecionar colunas finais
    final_cols = ['Area', 'Total de OSCs', '(%) Em relação ao total', '(%) Em relação ao grupo']
    df_display_area = df_area_table[final_cols].rename(columns={'Area': 'Áreas de Atuação'})

    # Renderizar HTML
    html_area = df_display_area.to_html(index=False, escape=False, classes='ipea-table')
    st.write(html_area, unsafe_allow_html=True)
    st.caption("Fonte: Mapa das OSCs (IPEA). Elaboração própria.")
    
    st.divider()

    # 1. Gráfico Geral das Áreas
    st.subheader("Gráfico 1 - Distribuição das OSCs por área de atuação")
    
    # Vamos usar nosso plotly para ser consistente
    fig_area = plot_bar_chart(df, 'Area_Atuacao', title="", orientation='v')
    # Remove legend
    fig_area.update_layout(showlegend=False)
    st.plotly_chart(fig_area, use_container_width=True)

    st.divider()

    # --- Tabela 5.1 (Original) - Natureza Jurídica ---
    import pandas as pd
    
    st.markdown("### Tabela 2 - Número de OSCs por natureza jurídica")

    # Mapeamento de Códigos de Natureza Jurídica (CONCLA/IBGE)
    # Fonte: https://concla.ibge.gov.br/estrutura/natjur-estrutura/natureza-juridica-2018.html
    nat_jur_map = {
        3999: 'Associação Privada',
        3069: 'Fundação Privada',
        3220: 'Organização Religiosa',
        3301: 'Organização Social (OS)',
        3130: 'Entidade Sindical',
        3105: 'Entidade de Mediação e Arbitragem',
        # Adicionar outros se aparecerem nos dados
    }

    target_col = 'cd_natureza_juridica_osc'
    
    # Fallback se a coluna padrão não existir, tenta procurar uma parecida
    if target_col not in df.columns:
         # Tenta achar alguma coluna que tenha 'natureza' no nome
         possible_cols = [c for c in df.columns if 'natureza' in c.lower()]
         if possible_cols:
             target_col = possible_cols[0]

    if target_col in df.columns:
        # Criar coluna descritiva se não existir
        if 'natureza_juridica_desc' not in df.columns:
            # Garantir que é numérico para usar o map (removendo traços se for string)
            def clean_code(x):
                try:
                    s = str(x).replace('-', '').replace('.', '')
                    return int(s)
                except:
                    return 0
            
            df['temp_nat_code'] = df[target_col].apply(clean_code)
            df['Natureza Jurídica Desc'] = df['temp_nat_code'].map(nat_jur_map).fillna(df[target_col].astype(str))
        else:
            df['Natureza Jurídica Desc'] = df['natureza_juridica_desc']

        # Calcular estatísticas
        total_geral = len(df)
        df_nat = df['Natureza Jurídica Desc'].value_counts().reset_index()
        df_nat.columns = ['Natureza Jurídica', 'Total de OSCs']
        
        # Calcular Porcentagens
        df_nat['(%) Em relação ao total'] = (df_nat['Total de OSCs'] / total_geral * 100).round(1)
        df_nat['(%) Em relação ao grupo'] = "100.0"

        # Adicionar linha de Total
        row_total = pd.DataFrame({
            'Natureza Jurídica': ['<b>Total Geral</b>'],
            'Total de OSCs': [total_geral],
            '(%) Em relação ao total': [100.0],
            '(%) Em relação ao grupo': ['-']
        })
        
        df_display = pd.concat([df_nat, row_total], ignore_index=True)

        # Formatação
        df_display['Total de OSCs'] = df_display['Total de OSCs'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
        df_display['(%) Em relação ao total'] = df_display['(%) Em relação ao total'].astype(str)
        
        # HTML Styling
        html = df_display.to_html(index=False, escape=False, classes='ipea-table')
        
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
        st.warning(f"Coluna de Natureza Jurídica não encontrada. Colunas disponíveis: {list(df.columns)}")

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
