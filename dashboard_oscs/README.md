# Dashboard de Análise de OSCs de Santos 🏙️

Este projeto é um dashboard interativo desenvolvido em Python com Streamlit para analisar dados das Organizações da Sociedade Civil (OSCs) de Santos.

## 📋 Funcionalidades

O dashboard está organizado nas seguintes páginas:

1.  **Overview**: Visão geral com KPIs, distribuição por Natureza Jurídica e Ano de Fundação.
2.  **Áreas de Atuação**: Análise das áreas de atuação (Saúde, Educação, Cultura, etc.) com detalhamento por subáreas.
3.  **Geolocalização**: Mapa interativo com filtros para explorar a distribuição territorial das OSCs.
4.  **Situação Cadastral**: Gráficos sobre o status (Ativa, Inapta, Suspensa) das organizações.
5.  **Tendências**: Série histórica da criação de novas OSCs na cidade.

## 📂 Estrutura do Projeto

```
dashboard_oscs/
├── data/               # Dados brutos (CSV)
├── pages/              # Scripts das páginas do dashboard
├── utils/              # Módulos de utilidades (limpeza, carregamento, gráficos)
├── app.py              # Ponto de entrada da aplicação
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

## 🚀 Instalação e Execução

### Pré-requisitos

Certifique-se de ter o Python instalado (versão 3.8 ou superior).

### 1. Instalar Dependências

No terminal, navegue até a pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 2. Rodar o Dashboard

Execute o comando:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

## 📊 Fonte de Dados

Os dados utilizados (`oscs_santos.csv`) contém informações cadastrais, geográficas e de áreas de atuação das OSCs de Santos.
