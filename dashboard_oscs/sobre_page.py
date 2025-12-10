
import streamlit as st
from dashboard_utils.styles import apply_academic_style


# Note: st.set_page_config should NOT be called here if it's called in the main app.py routing
# But for individual page testing it might be useful.
# However, within st.navigation, page config is usually handled by the main app or the first page load.
# Let's keep the content focus.

apply_academic_style()

st.title("Relatório preliminar das OSCIPs e OSs de Santos")

st.markdown("""
Este relatório apresenta um panorama inicial das OSCs em Santos, abrangendo informações desde 1930 até 2025. O levantamento, de caráter preliminar, consolida dados do Mapa das OSCs (IPEA) (https://mapaosc.ipea.gov.br/), do sistema de prestação de contas da Prefeitura de Santos (https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas) e, por fim, utiliza dados da Relação Anual de Informações Sociais (Rais) (https://basedosdados.org/dataset/3e7c4d58-96ba-448e-b053-d385a829ef00?table=dabe5ea8-3bb5-4a3e-9d5a-3c7003cd4a60), com recorte na cidade de Santos e foco nas naturezas jurídicas das organizações identificadas como OSCs. O documento serve como base para estudos futuros.

---
**Use o menu lateral para navegar entre as páginas de análise.**
""")

