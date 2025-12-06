import streamlit as st

st.set_page_config(
    page_title="Dashboard OSCs Santos",
    layout="wide"
)
from utils.styles import apply_academic_style
apply_academic_style()



st.title("Relatório preliminar das OSCIPs e OSs de Santos")

st.markdown("""
O relatório de pesquisa apresenta um panorama inicial sobre as Organizações da Sociedade Civil (OSCs) atuantes no município de Santos, abrangendo informações de 1930 até 2025. É um levantamento preliminar que servirá como base para estudos posteriores.

A principal fonte documental são dados secundários obtidos a partir da plataforma oficial 'Mapa das Organizações da Sociedade Civil (Mapa das OSCs)' (https://mapaosc.ipea.gov.br/), mantido pelo Instituto de Pesquisa Econômica Aplicada (Ipea).

**Palavras-chave**: OSC. Terceiro Setor. Fundo Público. Serviço Social. Santos.

st.markdown("---")
st.subheader("Navegação")
st.markdown("Acesse as páginas do painel através dos botões abaixo:")

st.page_link("pages/1_Visao_Geral.py", label="Visão Geral", icon="📊", use_container_width=True)
st.page_link("pages/2_Areas_de_Atuacao.py", label="Áreas de Atuação", icon="🎭", use_container_width=True)
st.page_link("pages/3_Geolocalizacao.py", label="Geolocalização", icon="🗺️", use_container_width=True)
st.page_link("pages/4_Situacao_Cadastral.py", label="Situação Cadastral", icon="📝", use_container_width=True)
st.page_link("pages/5_Tendencias.py", label="Tendências", icon="📈", use_container_width=True)
st.page_link("pages/6_Evolucao_Temporal_Mapa.py", label="Evolução Temporal Mapa", icon="⏳", use_container_width=True)
st.page_link("pages/7_Repasses_Federais.py", label="Repasses Federais", icon="🏛️", use_container_width=True)
st.page_link("pages/7_Repasses_Prefeitura.py", label="Repasses Prefeitura", icon="💰", use_container_width=True)