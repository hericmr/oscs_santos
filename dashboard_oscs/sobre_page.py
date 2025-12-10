import streamlit as st
from dashboard_utils.styles import apply_academic_style

apply_academic_style()

# Título ajustado para maior impacto
st.title("Relatório Preliminar: OSCs, OSCIPs e OSs em Santos")

# Texto introdutório com justificação (HTML/CSS inline para estilo acadêmico)
st.markdown("""
<div style="text-align: justify;">
Este relatório apresenta um panorama inicial das Organizações da Sociedade Civil (OSCs) em Santos, 
abrangendo informações desde 1930 até 2025. O levantamento, de caráter preliminar, consolida dados 
de três bases principais, servindo como alicerce para estudos futuros sobre o terceiro setor na região.
</div>
<br>
""", unsafe_allow_html=True)

# Destaque para as fontes de dados (Metodologia)
with st.container():
    st.subheader("Fontes de Dados")
    st.markdown("""    
    1. **[Mapa das OSCs (IPEA)](https://mapaosc.ipea.gov.br/)**: Dados nacionais filtrados para o município.
    2. **[Prefeitura de Santos (Prestação de Contas)](https://egov.santos.sp.gov.br/dadosabertos/prestacao_contas)**: Dados do sistema de transparência municipal.
    3. **[Relação Anual de Informações Sociais - RAIS (via Base dos Dados)](https://basedosdados.org/dataset/3e7c4d58-96ba-448e-b053-d385a829ef00?table=dabe5ea8-3bb5-4a3e-9d5a-3c7003cd4a60)**: Recorte focado nas naturezas jurídicas das organizações identificadas como OSCs.
    """)

# Separador visual e instrução de navegação discreta
st.divider()

# Usando st.info ou st.warning para instruções de UI (User Interface)
st.info("<--- **Navegação:** Utilize o menu lateral para acessar os gráficos e as análises detalhadas.")
