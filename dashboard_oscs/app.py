import streamlit as st
import sys
import os

# Add current directory to path to ensure dashboard_utils is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuração da Página Principal (Navigation)
st.set_page_config(page_title="Dashboard OSCs Santos", layout="wide")

# Definição das Páginas
pg = st.navigation([
    st.Page("sobre_page.py", title="1. Sobre"),
    st.Page("pages/1_Visao_Geral.py", title="2. Visão Geral"),
    st.Page("pages/2_Areas_de_Atuacao.py", title="3. Áreas de Atuação"),
    st.Page("pages/3_Mapa_Geral.py", title="4. Mapa Geral"),
    st.Page("pages/4_Situacao_Cadastral.py", title="5. Situação Cadastral"),
    st.Page("pages/5_Tendencias.py", title="6. Tendências"),
    st.Page("pages/6_Mapa_Evolucao.py", title="7. Mapa Evolução"),
    st.Page("pages/7_Repasses_Federais.py", title="8. Repasses Federais"),
    st.Page("pages/7_Repasses_Prefeitura.py", title="9. Repasses Prefeitura"),
    st.Page("pages/8_Correspondencia_Repasses.py", title="10. Correspondência Repasses"),
    st.Page("pages/9_Mapa_Repasses.py", title="11. Mapa Repasses")
])

pg.run()