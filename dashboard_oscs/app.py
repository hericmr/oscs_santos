import streamlit as st

st.set_page_config(
    page_title="Dashboard OSCs Santos",
    layout="wide"
)

# --- BLOCO DE ESTILO CSS (ACADÊMICO) ---
# Isso força a fonte Times New Roman em todo o app e justifica o texto
st.markdown("""
    <style>
    /* Altera a fonte de todo o sistema para Times New Roman */
    html, body, [class*="css"] {
        font-family: 'Times New Roman', Times, serif;
    }
    
    /* Justifica os parágrafos de texto (padrão ABNT) */
    .stMarkdown p {
        text-align: justify;
        font-size: 18px; /* Um pouco maior para leitura */
        line-height: 1.6; /* Espaçamento entre linhas confortável */
    }
    
    /* Ajusta cor dos títulos para preto absoluto */
    h1, h2, h3 {
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
# ----------------------------------------

st.title("Mapeamento Crítico das OSCs de Santos")

st.markdown("""
O presente relatório de pesquisa tem o objetivo de apresentar alguns dados das Organizações da Sociedade Civil - OSCs santistas - (de 1930 até 2025). E subsidiará análises futuras mais detalhadas. A investigação usa fontes documentais e dados secundários provenientes do Mapa das OSCs (IPEA) e do Portal da Transparência da Prefeitura de Santos.

Para a identificação e mapeamento das Organizações da Sociedade Civil (OSCs) que atuam no município de Santos, este estudo utilizará dados provenientes da plataforma Mapa das Organizações da Sociedade Civil (Mapa das OSC), desenvolvida e mantida pelo Instituto de Pesquisa Econômica Aplicada (Ipea). Desde 2016, o Ipea é o responsável legal pela organização das estatísticas públicas referentes às OSCs no Brasil, conforme estabelecido pelo Decreto nº 8.726/2016, que regulamenta a Lei nº 13.019/2014, o Marco Regulatório das Organizações da Sociedade Civil (MROSC). Essa plataforma pública reúne informações oficiais do Cadastro Nacional da Pessoa Jurídica (CNPJ), da Relação Anual de Informações Sociais (RAIS) e de bases setoriais e é reconhecida como a fonte mais completa e metodologicamente robusta sobre o universo das OSCs no país (IPEA, 2021).

**Palavras-chave**: OSC. Terceiro Setor. Fundo Público. Serviço Social. Santos.

---
**Use o menu lateral para navegar entre as páginas de análise.**
""")