import streamlit as st
from streamlit_folium import st_folium
from dashboard_utils.data_loader import load_data
from dashboard_utils.visualizations import plot_map


from dashboard_utils.styles import apply_academic_style
apply_academic_style()

st.title("Mapa 1 - Distribuição geográfica das OSs e OSCIPs em Santos")

df = load_data()

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("Filtros")
    
    avail_areas = sorted(list(df['Area_Atuacao'].unique())) if 'Area_Atuacao' in df.columns else []
    selected_areas = st.sidebar.multiselect("Área de Atuação", avail_areas, default=avail_areas)
    
    avail_sit = sorted(list(df['situacao_cadastral'].unique())) if 'situacao_cadastral' in df.columns else []
    selected_sit = st.sidebar.multiselect("Situação Cadastral", avail_sit, default=['Ativa'] if 'Ativa' in avail_sit else avail_sit)

    # Apply Filters
    df_filtered = df.copy()
    if 'Area_Atuacao' in df.columns and selected_areas:
        df_filtered = df_filtered[df_filtered['Area_Atuacao'].isin(selected_areas)]
    
    if 'situacao_cadastral' in df.columns and selected_sit:
        df_filtered = df_filtered[df_filtered['situacao_cadastral'].isin(selected_sit)]
        
    st.info(f"Mostrando {len(df_filtered)} OSCs no mapa.")
    
    # Map
    if not df_filtered.empty:
        # Colunas e Labels para o Popup
        cols_to_show = {
            'tx_razao_social_osc': 'Razão Social',
            'dt_fundacao_osc': 'Fundação',
            'Area_Atuacao': 'Área de Atuação',
            'situacao_cadastral': 'Situação',
            'tx_endereco_completo': 'Endereço',
            'cd_natureza_juridica_osc': 'Natureza Jurídica',
            'cnpj': 'CNPJ' # Se disponível
        }
        
        m = plot_map(df_filtered, tooltip_cols=cols_to_show)
        if m:
            st_folium(m, width="100%", height=600)
        else:
            st.warning("Não há coordenadas válidas para os filtros selecionados.")
    else:
        st.warning("Nenhum resultado encontrado com os filtros atuais.")

else:
    st.error("Erro ao carregar dados.")
