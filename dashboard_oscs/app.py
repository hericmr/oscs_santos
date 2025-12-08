import streamlit as st

# Configuração da Página Principal (Navigation)
st.set_page_config(page_title="Dashboard OSCs Santos", layout="wide")

# Definição das Páginas
pg = st.navigation([
    st.Page("sobre_page.py", title="Sobre", icon="ℹ️"),
    st.Page("pages/1_Visao_Geral.py", title="Visão Geral", icon="📊"),
    st.Page("pages/2_Areas_de_Atuacao.py", title="Áreas de Atuação", icon="🎯"),
    st.Page("pages/3_Mapa_Geral.py", title="Mapa Geral", icon="🗺️"),
    st.Page("pages/4_Situacao_Cadastral.py", title="Situação Cadastral", icon="📋"),
    st.Page("pages/5_Tendencias.py", title="Tendências", icon="📈"),
    st.Page("pages/6_Mapa_Evolucao.py", title="Mapa Evolução", icon="⏳"),
    st.Page("pages/7_Repasses_Federais.py", title="Repasses Federais", icon="🏛️"),
    st.Page("pages/7_Repasses_Prefeitura.py", title="Repasses Prefeitura", icon="🏙️"),
    st.Page("pages/8_Correspondencia_Repasses.py", title="Correspondência Repasses", icon="🔗"),
    st.Page("pages/9_Mapa_Repasses.py", title="Mapa Repasses", icon="📍")
])

pg.run()