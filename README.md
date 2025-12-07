# Mapeamento Crítico das Organizações da Sociedade Civil em Santos

![Status do Projeto](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

Este projeto tem como objetivo realizar um mapeamento e uma análise crítica das Organizações da Sociedade Civil (OSCs) na cidade de Santos-SP. A iniciativa combina processamento de dados governamentais, análise estatística e visualização interativa para fornecer insights sobre a distribuição territorial, a evolução histórica e o fluxo de recursos públicos (prestação de contas) dessas entidades.

##  Objetivos

- **Mapear** a distribuição geespacial e temática das OSCs no município.
- **Analisar** os dados de prestação de contas e repasses da Prefeitura de Santos (2018-2025).

## 📚 Fontes de Dados e Metadados

Os dados apresentados neste dashboard são consolidados a partir de duas fontes primárias:

### 1. Mapa das Organizações da Sociedade Civil (IPEA)
- **Fonte**: Base de dados oficial do IPEA (Instituto de Pesquisa Econômica Aplicada).
- **Dados Extraídos**: Cadastro nacional de OSCs, incluindo CNPJ, Razão Social, endereço, área de atuação e natureza jurídica.
- **Processamento**: Os dados foram filtrados para o município de Santos-SP e enriquecidos com geolocalização.

### 2. Portal de Dados Abertos de Santos (Prefeitura Municipal)
- **Fonte**: [Portal de Dados Abertos - Santos](https://egov.santos.sp.gov.br/dadosabertos)
- **Dados Extraídos**: 
    - Recursos transferidos para OSCs (valores de repasse, empenho).
    - Prestação de contas por ano, secretaria e entidade beneficiária.
- **Cobertura Temporal**: Dados completos de 2018 a 2025.


---

##  Estrutura do Repositório

O projeto está organizado para separar a lógica de processamento de dados (backend/scripts) da visualização (frontend/dashboard).

```plaintext
.
├── dashboard_oscs/             # Aplicação Web Interativa (Streamlit)
│   ├── pages/                  # Páginas individuais do dashboard
│   ├── utils/                  # Funções auxiliares de carga e plotagem
│   └── app.py                  # Ponto de entrada do Dashboard
│
├── scripts/                    # Scripts de ETL e Análise Estatística
│   ├── filter_brazil_data.py   # Filtra dados do IPEA (Nacional -> Local)
│   ├── generate_analysis.py    # Gera relatórios estatísticos gerais
│   └── analisar_dados.py       # Script específico de Prestação de Contas
│
├── dados_completos/            # Dados Brutos (Raw Data)
│   ├── *.json / *.csv          # Arquivos originais (PM Santos/IPEA)
│   └── indice_downloads.json   # Controle de downloads
│
├── dados_atualizados/          # Dados Processados (Clean Data)
│   # Repositório de CSVs limpos utilizados pelo Dashboard
│
├── analises/                   # Relatórios de Texto/CSV gerados pelos scripts
│   ├── relatorio_por_ano.csv
│   ├── relatorio_por_secretaria.csv
│   └── relatorio_por_beneficiaria.csv
│
├── graficos/                   # Exportação de gráficos estáticos (Matplotlib/Seaborn)
└── requirements.txt            # Dependências do projeto