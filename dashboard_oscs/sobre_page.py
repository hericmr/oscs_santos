import streamlit as st
from dashboard_utils.styles import apply_academic_style

apply_academic_style()

# Título ajustado para maior impacto
st.title("Relatório Preliminar: OSCs, OSCIPs e OSs em Santos")

# Texto introdutório com justificação (HTML/CSS inline para estilo acadêmico)
st.markdown("""
<div style="text-align: justify;">
Este relatório apresenta um panorama inicial das OSCs em Santos, abrangendo informações 
desde 1930 até 2025. O levantamento, de caráter preliminar, consolida dados do 
Mapa das OSCs (IPEA), da página de prestação de contas da Prefeitura de Santos e 
dos dados da Relação Anual de Informações Sociais (Rais), com recorte na cidade
de Santos e foco nas naturezas jurídicas das organizações identificadas como OSCs. 
O documento serve como base para estudos futuros.
</div>
<br>
""", unsafe_allow_html=True)

# Destaque para as fontes de dados (Metodologia)
with st.container():
    st.subheader("Fontes de dados")
    st.markdown("""    
    1. **[Mapa das OSCs (IPEA)](https://mapaosc.ipea.gov.br/)**
    2. **[Prefeitura de Santos (Prestação de Contas)](https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas)**
    3. **[Relação Anual de Informações Sociais - RAIS (via Base dos Dados)](https://basedosdados.org/dataset/3e7c4d58-96ba-448e-b053-d385a829ef00?table=dabe5ea8-3bb5-4a3e-9d5a-3c7003cd4a60)**
    """)

# Separador visual e instrução de navegação discreta
st.divider()

# Usando st.info ou st.warning para instruções de UI (User Interface)
st.info("<--- **Navegação:** Utilize o menu lateral para acessar os gráficos e as análises detalhadas.")
