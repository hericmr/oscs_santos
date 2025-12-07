# Mapeamento Crítico das Organizações da Sociedade Civil em Santos

![Status do Projeto](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

Este projeto tem como objetivo realizar um mapeamento e uma análise crítica das Organizações da Sociedade Civil (OSCs) na cidade de Santos-SP. A iniciativa combina processamento de dados governamentais, análise estatística e visualização interativa para fornecer insights sobre a distribuição territorial, a evolução histórica e o fluxo de recursos públicos (prestação de contas) dessas entidades.

##  Objetivos

- **Mapear** a distribuição geespacial e temática das OSCs no município.
- **Analisar** os dados de prestação de contas e repasses da Prefeitura de Santos (2018-2025).

## Fontes de Dados e Metadados

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

## Metodologia e Pipeline de Tratamento de Dados

Para garantir a validade científica e a reprodutibilidade da pesquisa, este projeto documenta rigorosamente como os dados brutos foram transformados em informação analítica. O objetivo é afastar qualquer dúvida sobre a integridade dos números apresentados.

### 1. Definição das Fontes (Origem)
O projeto cruza duas bases de dados distintas para gerar as informações do dashboard:
- **Base Transacional**: Dados de Prestação de Contas da Prefeitura de Santos (Portal de Dados Abertos) - Foco em valores repassados, datas das transações e secretarias responsáveis.
- **Base Cadastral**: Mapa das OSCs (IPEA) - Foco na caracterização da entidade, incluindo natureza jurídica, área de atuação oficial e data de fundação.

### 2. Processo de Higienização (Data Cleaning)
A integridade dos dados é assegurada pelas seguintes etapas de normalização:
- **Chave Primária (CNPJ)**: Remoção de caracteres especiais (pontos, traços, barras) via *Regex* para garantir um formato numérico puro (14 dígitos). Isso é crucial para permitir o cruzamento exato entre bases que utilizam formatações diferentes.
- **Normalização Monetária**: Conversão de strings de texto (ex: "R$ 1.000,00") para *float* (ponto flutuante), garantindo a precisão matemática das somas e médias calculadas.
- **Normalização Temporal**: Conversão de formatos de data variados para objetos *datetime* padrão (ISO 8601), essencial para a construção correta das séries temporais.

### 3. Estratégia de Cruzamento (Merge/Enriquecimento)
- **Método**: Foi realizado um cruzamento do tipo *Left Join*, onde a tabela da Prefeitura atua como âncora (esquerda) e a tabela do IPEA (direita) enriquece os registros.
- **Dados Faltantes**: Entidades que receberam verba da prefeitura mas não constam na base do IPEA federal foram categorizadas como **"Não Classificadas"**. Essa estratégia evita o descarte de registros financeiros válidos e não mascara a informação, mantendo a fidelidade aos valores totais repassados.

### 4. Reprodutibilidade
Todos os scripts de processamento (ETL) estão disponíveis publicamente neste repositório, permitindo a auditoria do código e a replicação dos resultados por outros pesquisadores interessados na validação da metodologia.

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