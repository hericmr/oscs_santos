# Guia de Implantação (Deployment)

O **Streamlit** é uma aplicação que roda em Python, o que significa que ele precisa de um servidor ativo para processar os dados e gerar os gráficos. Por isso, serviços de hospedagem estática como **GitHub Pages** ou **Google Sites** (Google Pages) **não funcionam** diretamente para este tipo de dashboard.

Aqui estão as melhores opções gratuitas ou de baixo custo para colocar seu site online:

## Opção 1: Streamlit Community Cloud (Recomendada e Gratuita)
A maneira mais fácil e oficial de hospedar aplicativos Streamlit.

### Passos:
1.  **Crie um repositório no GitHub**:
    - Se ainda não tiver, crie uma conta no [GitHub](https://github.com/).
    - Crie um novo repositório e suba os arquivos do seu projeto (pasta `dashboard_oscs`, `requirements.txt`, etc.).
2.  **Acesse o Streamlit Cloud**:
    - Vá para [share.streamlit.io](https://share.streamlit.io/).
    - Faça login com seu GitHub.
3.  **Deploy**:
    - Clique em "New app".
    - Selecione o repositório, a branch (ex: `main`) e o arquivo principal (`dashboard_oscs/app.py`).
    - Clique em "Deploy".

O Streamlit Cloud instalará automaticamente as bibliotecas do `requirements.txt` e colocará seu site no ar.

## Opção 2: Google Cloud Run (Se você precisa usar Google)
Se você prefere usar a infraestrutura do Google, pode usar o Cloud Run, mas é um pouco mais técnico (requer Docker).

### Passos Rápidos:
1.  Crie um `Dockerfile` na raiz do projeto:
    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /app
    COPY . .
    RUN pip install -r dashboard_oscs/requirements.txt
    EXPOSE 8080
    CMD ["streamlit", "run", "dashboard_oscs/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
    ```
2.  Instale o [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
3.  Faça o deploy via terminal:
    ```bash
    gcloud run deploy --source .
    ```

## Resumo
Para sair do zero rapidamente, use a **Opção 1 (Streamlit Community Cloud)**. É feita exatamente para isso.
