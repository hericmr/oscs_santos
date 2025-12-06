# Análise de Dados - Prestação de Contas Prefeitura de Santos

## 📊 Sobre o Projeto

Este projeto contém dados de prestação de contas da Prefeitura Municipal de Santos, coletados do portal de dados abertos.

## 📁 Estrutura do Projeto

```
.
├── dados_completos/          # Dados brutos (JSON e CSV)
│   ├── *.json               # Dados em formato JSON
│   ├── *.csv                # Dados convertidos para CSV
│   └── indice_downloads.json # Índice dos downloads
├── analise/                  # Resultados das análises (gerado automaticamente)
├── analisar_dados.py        # Script principal de análise
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar Análise

```bash
python3 analisar_dados.py
```

O script irá:
- Carregar todos os dados de prestação de contas
- Gerar estatísticas descritivas
- Criar relatórios em CSV na pasta `analise/`

## 📈 Dados Disponíveis

### Período
- **Anos**: 2018-2025
- **Total de registros**: Milhares de registros

### Campos Principais
- `ano`: Ano de referência
- `secretaria_sigla`: Sigla da secretaria
- `beneficiaria_nome`: Nome da beneficiária
- `valor_recurso`: Valor do recurso
- `valor_repasse`: Valor do repasse

## 📊 Relatórios Gerados

Após executar `analisar_dados.py`, os seguintes relatórios serão gerados em `analise/`:

1. **relatorio_por_ano.csv** - Agregação de valores por ano
2. **relatorio_por_secretaria.csv** - Agregação por secretaria
3. **relatorio_por_beneficiaria.csv** - Agregação por beneficiária

### Estatísticas Atuais

- **Total de registros**: 7.848
- **Período**: 2018-2025
- **Valor total de recursos**: R$ 27,7 bilhões
- **Valor total de repasses**: R$ 1,9 bilhões
- **Top 3 Secretarias**: SEDUC (2.986 registros), SMS (1.609), SEDS (1.460)

## 🔧 Personalização

Você pode modificar o script `analisar_dados.py` para:
- Adicionar novas análises
- Criar visualizações (gráficos)
- Exportar para outros formatos (Excel, etc.)
- Filtrar dados por critérios específicos

## 📝 Notas

- Os dados foram coletados do portal oficial: https://egov.santos.sp.gov.br/dadosabertos
- Os dados mais completos são de 2021-2025
- Alguns anos podem ter menos registros

## 📄 Licença

Dados públicos da Prefeitura Municipal de Santos.
