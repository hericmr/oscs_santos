## 📁 Estrutura Atual

```
webscrapp_prefeitura/
├── dados_completos/          # Dados brutos coletados
│   ├── *.json               # 26 arquivos JSON
│   ├── *.csv                # 23 arquivos CSV
│   ├── indice_downloads.json # Índice dos downloads
│   └── urls_encontradas.txt  # URLs das APIs encontradas
│
├── analise/                  # Resultados das análises
│   ├── relatorio_por_ano.csv
│   ├── relatorio_por_secretaria.csv
│   └── relatorio_por_beneficiaria.csv
│
├── README.md                 # Documentação principal
└── ESTRUTURA_PROJETO.md     # Este arquivo
```

## 📊 Dados Disponíveis

### Prestação de Contas
- **7.848 registros** no total
- **Período**: 2018-2025
- **Valor total de recursos**: R$ 27,7 bilhões
- **Valor total de repasses**: R$ 1,9 bilhões

### Outros Dados
- Despesas por ação
- Detalhamento de despesas
- Receitas próprias

## 🚀 Próximos Passos

1. **Análise Exploratória**: Use `analisar_dados.py` para gerar estatísticas
2. **Visualizações**: Adicione gráficos usando matplotlib/plotly
3. **Análises Específicas**: Crie scripts para análises customizadas
4. **Exportação**: Exporte para Excel ou outros formatos conforme necessário

## 📝 Notas

- Todos os dados estão em `dados_completos/`
- Os relatórios são gerados automaticamente em `analise/`
- O script de análise pode ser customizado conforme suas necessidades

