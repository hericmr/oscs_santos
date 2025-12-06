# Mapeamento Crítico das Organizações da Sociedade Civil em Santos

Este projeto tem como objetivo realizar um mapeamento e análise crítica das Organizações da Sociedade Civil (OSCs) na cidade de Santos. O projeto combina processamento de dados, análise estatística e visualização interativa para fornecer insights sobre a distribuição, evolução e características das OSCs locais.

## 📂 Estrutura do Projeto

A estrutura de diretórios do projeto é organizada da seguinte forma:

- **[dashboard_oscs/](dashboard_oscs/)**: Contém o código fonte do dashboard interativo desenvolvido com Streamlit.
    - `app.py`: Arquivo principal da aplicação Streamlit.
    - `pages/`: Páginas individuais do dashboard.
    - `utils/`: Funções utilitárias para carregamento de dados e visualização.
- **[scripts/](scripts/)**: Scripts Python utilizados para limpeza de dados, processamento e geração de análises estáticas.
    - `filter_brazil_data.py`: Filtra dados nacionais para o contexto local.
    - `generate_analysis.py`: Gera relatórios de texto com análises estatísticas.
- **[analises/](analises/)**: Diretório onde são salvos os relatórios de texto gerados pelos scripts de análise.
- **[graficos/](graficos/)**: Diretório para armazenamento de gráficos estáticos gerados (ex: Matplotlib/Seaborn).
- **[dados atualizados/](dados%20atualizados/)**: Repositório de arquivos de dados (CSV, etc.) utilizados e gerados pelo projeto.

## 🚀 Instalação

Para executar as ferramentas deste projeto, você precisará ter o Python instalado. É recomendado o uso de um ambiente virtual.

1.  **Clone o repositório** (se aplicável) ou navegue até a pasta do projeto.
2.  **Instale as dependências**:
    As dependências principais do dashboard estão listadas em `dashboard_oscs/requirements.txt`.

    ```bash
    pip install -r dashboard_oscs/requirements.txt
    ```

    Para os scripts de análise na pasta `scripts/`, bibliotecas adicionais de ciência de dados (como pandas, matplotlib, seaborn) podem ser necessárias.

## 🖥️ Como Usar

### Executando o Dashboard

O dashboard é a principal interface para exploração dos dados. Para iniciá-lo:

1.  Navegue até a pasta do dashboard:
    ```bash
    cd dashboard_oscs
    ```
2.  Execute o Streamlit:
    ```bash
    streamlit run app.py
    ```

### Executando Scripts de Análise

Os scripts na pasta `scripts/` podem ser executados individualmente para realizar tarefas específicas de processamento de dados ou atualização de relatórios.

Exemplo:
```bash
python scripts/generate_analysis.py
```

## 📊 Metodologia

O projeto utiliza dados públicos de OSCs, padroniza as informações e aplica classificações (como Áreas de Atuação e Natureza Jurídica) para permitir análises comparativas e temporais.
