import streamlit as st

st.set_page_config(
    page_title="Dashboard OSCs Santos",
    layout="wide"
)
from utils.styles import apply_academic_style
apply_academic_style()



st.title("Mapeamento Crítico das OSCs de Santos")

st.markdown("""
O relatório de pesquisa apresenta um panorama inicial sobre as Organizações da Sociedade Civil (OSCs) atuantes no município de Santos, abrangendo informações de 1930 até 2025. É um levantamento preliminar que servirá como base para estudos posteriores.

A principal fonte documental são dados secundários obtidos a partir da plataforma oficial 'Mapa das Organizações da Sociedade Civil (Mapa das OSCs)' (https://mapaosc.ipea.gov.br/), mantido pelo Instituto de Pesquisa Econômica Aplicada (Ipea).

**Palavras-chave**: OSC. Terceiro Setor. Fundo Público. Serviço Social. Santos.

---
**Use o menu lateral para navegar entre as páginas de análise.**
""")