import streamlit as st
from utils.styles import apply_academic_style

# Note: st.set_page_config should NOT be called here if it's called in the main app.py routing
# But for individual page testing it might be useful.
# However, within st.navigation, page config is usually handled by the main app or the first page load.
# Let's keep the content focus.

apply_academic_style()

st.title("Relatório preliminar das OSCIPs e OSs de Santos")

st.markdown("""
Este relatório apresenta um panorama inicial das OSCs em Santos, abrangendo informações desde 1930 até 2025. O levantamento, de caráter preliminar, consolida dados do Mapa das OSCs (IPEA) (https://mapaosc.ipea.gov.br/)e do sistema de prestação de contas da Prefeitura de Santos (https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas), servindo como base estratégica para estudos futuros.

---
**Use o menu lateral para navegar entre as páginas de análise.**
""")
