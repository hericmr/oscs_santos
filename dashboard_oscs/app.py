import streamlit as st
import sys
import os

# Add current directory to path to ensure dashboard_utils is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import custom GUI utils for Responsive Menu
try:
    from dashboard_utils.gui import inject_mobile_detection, is_mobile_device, render_mobile_header
except ImportError:
    # Fallback if module issue, though unlikely with sys.path set
    st.error("Erro ao carregar módulo de interface (dashboard_utils.gui).")
    inject_mobile_detection = lambda: None
    is_mobile_device = lambda: False
    render_mobile_header = lambda p: None

# Configuração da Página Principal
st.set_page_config(page_title="Relatório OSCs Santos", layout="wide")

# -----------------------------------------------------------------------------
# RESPONSIVE MENU LOGIC
# -----------------------------------------------------------------------------

# 1. Inject JS to detect screen width and update URL query params if needed
inject_mobile_detection()

# 2. Determine current mode (Desktop or Mobile) based on query param
mobile_mode = is_mobile_device()

# 3. Define all Pages
pages = [
    st.Page("sobre_page.py", title="1. Sobre"),
    st.Page("pages/1_Visao_Geral.py", title="2. Visão Geral"),
    st.Page("pages/2_Areas_de_Atuacao.py", title="3. Áreas de Atuação"),
    st.Page("pages/3_Mapa_Geral.py", title="4. Mapa Geral"),
    st.Page("pages/4_Situacao_Cadastral.py", title="5. Situação Cadastral"),
    st.Page("pages/5_Tendencias.py", title="6. Tendências"),
    st.Page("pages/6_Mapa_Evolucao.py", title="7. Evolução Quantitativa das OSC"),
    st.Page("pages/7_Repasses_Federais.py", title="8. Transferências de Recursos Públicos Federais"),
    st.Page("pages/7_Repasses_Prefeitura.py", title="9. Transferências de Recursos Públicos Municipais"),
    st.Page("pages/8_Correspondencia_Repasses.py", title="10. Correspondência de Transferências"),
    st.Page("pages/9_Mapa_Repasses.py", title="11. Evolução Quantitativa das Transferências")
]

# 4. Configure Navigation based on mode
if mobile_mode:
    # MOBILE: Hide standard sidebar, rendering handled by render_mobile_header below
    pg = st.navigation(pages, position="hidden")
else:
    # DESKTOP: Standard sidebar navigation
    pg = st.navigation(pages, position="sidebar")

# 5. Render Mobile Header if in mobile mode
if mobile_mode:
    render_mobile_header(pages)

# 6. Run the selected page
pg.run()