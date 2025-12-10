import streamlit as st
from dashboard_utils.data_loader import load_data
from dashboard_utils.visualizations import plot_bar_chart, plot_heatmap
import pandas as pd


from dashboard_utils.styles import apply_academic_style
apply_academic_style()

st.title("Áreas de Atuação")

df = load_data()

if not df.empty and 'Area_Atuacao' in df.columns:


    # --- Tabela: Áreas e Subáreas de Atuação (IPEA) ---
    # --- Tabela: Áreas e Subáreas de Atuação (IPEA) ---
    st.markdown("### Tabela 2 - Número de OSCs, segundo a finalidade de atuação (Atualizado)")
    st.markdown("Esta seção trata sobre as áreas de atuação das Organizações da Sociedade Civil - OSCs.")

    # --- Nova Implementação usando area_subarea.csv ---
    import os
    from dashboard_utils.data_loader import load_csv_robust
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Caminho para area_subarea.csv
    data_path_subarea = os.path.join(current_dir, '..', '..', 'dados atualizados', 'dados_filtrados', 'area_subarea.csv')
    
    if os.path.exists(data_path_subarea):
        try:
            # Carregar com robustez para encoding
            df_sub = load_csv_robust(data_path_subarea)
            
            # --- Mapeamento Completo e Detalhado ---
            # Keys: Nome Exibição da Área Pai
            # Values: Dict {'col_pai': 'NomeColPai', 'subareas': {'NomeExibicaoSub': 'NomeColSub', ...}}
            # AVISO: Usando 'contains' ou nomes parciais para evitar problemas com encoding exato (Ã§Ã£)
            
            # Helper para achar coluna que contem string
            def find_col(partial_name):
                matches = [c for c in df_sub.columns if partial_name in c]
                return matches[0] if matches else None

            # Construção da Estrutura de Dados
            structure = [
                {
                    "Area": "Habitação",
                    "ColPai": find_col("Habita") and find_col("Habita") if not find_col("Habita") is None else "Habitação", # Fallback logic handled inside loop
                    "Subareas": [
                        ("Habitação", "Hab sub Habita"),
                        ("Outros Habitação", "Hab sub Outros")
                    ]
                },
                {
                    "Area": "Saúde",
                    "ColPai": "SaÃºde", # Hardcoded based on debug, or use verify
                    "Subareas": [
                        ("Hospitais", "Saude sub Hospitais"),
                        ("Outros serviços de saúde", "Saude sub Outros serviÃ§os de saÃºde"),
                        ("Subárea Não Identificada", "Saude sub Outros") # Check duplicate 'Outros', maybe map specific logic
                    ]
                },
                {
                    "Area": "Cultura e recreação",
                    "ColPai": "Cultura e recrea",
                    "Subareas": [
                        ("Cultura e arte", "Cultura sub Cultura e arte"),
                        ("Esportes e recreação", "Cultura sub Esporte e recrea"),
                        ("Outros Cultura e recreação", "Cultura sub Outros")
                    ]
                },
                {
                    "Area": "Educação e pesquisa",
                    "ColPai": "EducaÃ§Ã£o e pesquisa",
                    "Subareas": [
                        ("Educação infantil", "Educacao sub EducaÃ§Ã£o infantil"),
                        ("Ensino fundamental", "Educacao sub Ensino fundamental"),
                        ("Ensino médio", "Educacao sub Ensino mÃ©dio"),
                        ("Ensino superior", "Educacao sub EducaÃ§Ã£o superior"),
                        ("Estudos e pesquisas", "Educacao sub Estudos e pesquisas"),
                        ("Educação profissional", "Educacao sub EducaÃ§Ã£o profissional"),
                        ("Outras formas de educação/ensino", "Educacao sub Outras formas de educaÃ§Ã£o/ensino"),
                        ("Atividades de apoio à educação", "Educacao sub Atividades de apoio Ã  educaÃ§Ã£o"),
                        ("Outros Educação e pesquisa", "Educacao sub Outros")
                    ]
                },
                {
                    "Area": "Assistência social",
                    "ColPai": "AssistÃªncia social",
                    "Subareas": [
                        ("Educação infantil", "Ass Social sub Educa"), # As vezes aparece duplicado entre areas, manter contexto
                        ("Assistência social", "Ass Social sub AssistÃªncia social"),
                        ("Outros Assistência social", "Ass Social sub Outros")
                    ]
                },
                {
                    "Area": "Religião",
                    "ColPai": "ReligiÃ£o",
                    "Subareas": [
                        ("Religião", "Religiao sub ReligiÃ£o"),
                        ("Outros Religião", "Religiao sub Outros")
                    ]
                },
                {
                    "Area": "Associações patronais e profissionais",
                    "ColPai": "AssociaÃ§Ãµes patronais",
                    "Subareas": [
                        ("Associações empresariais e patronais", "Ass Patronais sub AssociaÃ§Ãµes empresariais e patronais"),
                        ("Associações profissionais", "Ass Patronais sub AssociaÃ§Ãµes profissionais"),
                        ("Associações de produtores rurais, pescadores e similares", "Ass Patronais sub AssociaÃ§Ãµes de produtores rurais"),
                        ("Cooperativas sociais", "Ass Patronais sub Cooperativas sociais"),
                        ("Outras Associações patronais e profissionais", "Ass Patronais sub Outros")
                    ]
                },
                {
                    "Area": "Meio ambiente e proteção animal",
                    "ColPai": "Meio ambiente e prote",
                    "Subareas": [
                        ("Meio ambiente", "Meio Amb sub Meio ambiente"),
                        ("Proteção animal", "Meio Amb sub ProteÃ§Ã£o animal"),
                        ("Outros Meio ambiente e proteção animal", "Meio Amb sub Outros")
                    ]
                },
                {
                    "Area": "Desenvolvimento e defesa de direitos e interesses",
                    "ColPai": "Desenvolvimento e defesa de direitos",
                    "Subareas": [
                        ("Associações de moradores", "Desenv e Def sub AssociaÃ§Ãµes de moradores"),
                        ("Centros e associações comunitárias", "Desenv e Def sub Centros e associaÃ§Ãµes comunitÃ¡rias"),
                        ("Desenvolvimento rural", "Desenv e Def sub Desenvolvimento rural"),
                        ("Emprego e treinamento", "Desenv e Def sub Emprego e treinamento"),
                        ("Defesa de direitos de grupos e minorias", "Desenv e Def sub Defesa de direitos de grupos e minorias"),
                        ("Desenvolvimento e defesa de direitos", "Desenv e Def sub Desenvolvimento e defesa de direitos"), # Often repeated header as sub
                        ("Associações de pais, professores, alunos e afins", "Desenv e Def sub AssociaÃ§Ãµes de pais, professores, alunos e a"),
                        ("Associações patronais e profissionais", "Desenv e Def sub AssociaÃ§Ãµes patronais e profissionais"),
                        ("Cultura e recreação", "Desenv e Def sub Cultura e recreaÃ§Ã£o"),
                        ("Defesa de direitos e interesses - múltiplas áreas", "Desenv e Def sub Defesa de direitos e interesses - mÃºltiplas"),
                        ("Meio ambiente e proteção animal", "Desenv e Def sub Meio ambiente e proteÃ§Ã£o animal"),
                        ("Outras formas de desenvolvimento e defesa de direitos e interesses", "Desenv e Def sub Outras formas de desenvolvimento e defesa de d"),
                        ("Desenvolvimento e defesa de direitos e interesses - Religião", "Desenv e Def sub ReligiÃ£o"),
                        ("Saúde, assistência social e educação", "Desenv e Def sub SaÃºde, assistÃªncia social e educaÃ§Ã£o"),
                        ("Outros", "Desenv e Def sub Outros")
                    ]
                },
                {
                    "Area": "Outras atividades associativas",
                    "ColPai": "Outras atividades associativas",
                    "Subareas": [
                        ("Outras organizações da sociedade civil", "Outras sub AssociaÃ§Ãµes de atividades nÃ£o especificadas anter") # Mapping based on debug output for 'Outras sub...'
                    ]
                }
            ]

            table_rows = []
            total_oscs = len(df_sub)

            for item in structure:
                area_name = item["Area"]
                
                # Encontrar nome real da coluna pai no DF (partial match)
                real_col_pai = find_col(item["ColPai"]) if item["ColPai"] else None
                
                if real_col_pai and real_col_pai in df_sub.columns:
                    # Totais Pai
                    # Assumindo que 1 = Sim, nan/0 = Não.
                    # As colunas parecem vir vazias ou com 1.
                    # Debug output showed values like 1. Let's assume numeric sum is safer or check value '1'.
                    # Check first value type
                    # Keep it simple: non-null and containing '1' or numeric 1
                    count_pais = pd.to_numeric(df_sub[real_col_pai], errors='coerce').sum()
                    
                    if count_pais == 0:
                        # Se 0, ainda mostramos a linha se fizer parte da estrutura fixa solicitada
                        pass

                    pct_total_area = (count_pais / total_oscs) * 100

                    table_rows.append({
                        'Area': f"<b>{area_name}</b>",
                        'Total': count_pais,
                        'Perc_Total': pct_total_area,
                        'Perc_Group': None
                    })
                    
                    # Subareas
                    sub_total_check = 0
                    for sub_label, sub_partial_col in item["Subareas"]:
                        real_col_sub = find_col(sub_partial_col)
                        
                        if real_col_sub and real_col_sub in df_sub.columns:
                             # Count Only matching Parent? 
                             # The csv structure is flat but implies hierarchy.
                             # Let's count totals directly as filtering by parent might be redundant if data is clean,
                             # but strictly correct is to filter.
                             # df_filtered = df_sub[pd.to_numeric(df_sub[real_col_pai], errors='coerce') == 1]
                             # count_sub = pd.to_numeric(df_filtered[real_col_sub], errors='coerce').sum()
                             
                             # Actually, let's just sum the sub column.
                             count_sub = pd.to_numeric(df_sub[real_col_sub], errors='coerce').sum()
                             
                             if count_sub > 0:
                                 pct_total_sub = (count_sub / total_oscs) * 100
                                 if count_pais > 0:
                                     pct_group = (count_sub / count_pais) * 100
                                 else:
                                     pct_group = 0.0
                                 sub_total_check += count_sub
                                 
                                 table_rows.append({
                                    'Area': f"<span style='padding-left: 20px;'>{sub_label}</span>",
                                    'Total': count_sub,
                                    'Perc_Total': pct_total_sub,
                                    'Perc_Group': pct_group
                                })
                    
                    # Check for "Subárea Não Identificada" (Difference between Parent Total and Sum of Subs)
                    # If Sum Subs < Parent Total
                    if sub_total_check < count_pais:
                        diff = count_pais - sub_total_check
                        # Tolerance for float errors
                        if diff > 0.9: # at least 1
                             pct_total_unk = (diff / total_oscs) * 100
                             pct_group_unk = (diff / count_pais) * 100
                             table_rows.append({
                                    'Area': f"<span style='padding-left: 20px;'>Subárea Não Identificada</span>",
                                    'Total': diff,
                                    'Perc_Total': pct_total_unk,
                                    'Perc_Group': pct_group_unk
                             })

            # Add Grand Total
            table_rows.append({
                'Area': "<b>Total Geral de OSCs</b>",
                'Total': total_oscs,
                'Perc_Total': 100.0,
                'Perc_Group': None
            })
            
            # DataFrame Generation
            df_area_table = pd.DataFrame(table_rows)
            
            # Formatting
            df_area_table['Total de OSCs'] = df_area_table['Total'].apply(lambda x: f"{int(x):,.0f}".replace(",", "."))
            df_area_table['(%) Em relação ao total'] = df_area_table['Perc_Total'].apply(lambda x: f"{x:.1f}")
            df_area_table['(%) Em relação ao grupo'] = df_area_table['Perc_Group'].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "-")

            final_cols = ['Area', 'Total de OSCs', '(%) Em relação ao total', '(%) Em relação ao grupo']
            df_display_area = df_area_table[final_cols].rename(columns={'Area': 'Áreas de Atuação'})
            
            html_area = df_display_area.to_html(index=False, escape=False, classes='ipea-table')
            st.write(html_area, unsafe_allow_html=True)
            st.caption("Fonte: Mapa das OSCs (IPEA). Elaboração própria (Tabela Expandida).")

        except Exception as e:
            st.error(f"Erro ao processar tabela detalhada: {e}")
            st.write(e)
    else:
        st.error(f"Arquivo de dados detalhados não encontrado: {data_path_subarea}")
    
    st.divider()



    st.divider()

    # --- Tabela: Natureza Jurídica ---
    st.subheader("Tabela 6.1 - Número de OSCs segundo a natureza jurídica")
    
    # Mapeamento de Códigos de Natureza Jurídica (CONCLA/IBGE)
    # Fonte: https://concla.ibge.gov.br/estrutura/natjur-estrutura/natureza-juridica-2018.html
    nat_jur_map = {
        3999: 'Associação Privada',
        3069: 'Fundação Privada',
        3220: 'Organização Religiosa',
        3301: 'Organização Social (OS)',
        3130: 'Entidade Sindical',
        3105: 'Entidade de Mediação e Arbitragem',
    }
    
    # Utilizar a coluna correta
    target_col = 'cd_natureza_juridica_osc'
    
    if target_col in df.columns:
        # Prepara dados
        # Converter para numérico para o map funcionar
        def safe_int(x):
            try: return int(float(x))
            except: return 0
            
        df['temp_nat_code'] = df[target_col].apply(safe_int)
        df['Natureza Jurídica'] = df['temp_nat_code'].map(nat_jur_map).fillna(df[target_col].astype(str))
        
        # Agrupar e contar
        df_nat = df['Natureza Jurídica'].value_counts().reset_index()
        df_nat.columns = ['Natureza Jurídica', 'Quantidade']
        
        # Calcular Porcentagem
        total_nat = df_nat['Quantidade'].sum()
        df_nat['(%)'] = (df_nat['Quantidade'] / total_nat * 100)
        
        # Formatar
        df_nat['(%)'] = df_nat['(%)'].apply(lambda x: f"{x:.2f}%")
        
        # Adicionar linha TOTAL
        row_total = pd.DataFrame([{
            'Natureza Jurídica': 'TOTAL',
            'Quantidade': total_nat,
            '(%)': '100.00%'
        }])
        
        df_display_nat = pd.concat([df_nat, row_total], ignore_index=True)
         
        # Exibir Tabela
        st.table(df_display_nat)
        
        st.caption("Fonte: Mapa das Organizações da Sociedade Civil (Recorte Santos).")
    else:
        st.error(f"Coluna '{target_col}' não encontrada para gerar a tabela de Natureza Jurídica.")

    st.divider()



else:
    st.error("Dados de Área de Atuação indisponíveis.")
