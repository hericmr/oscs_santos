import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# Configuração de estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def clean_currency(x):
    if isinstance(x, str):
        return float(x.replace('R$', '').replace('.', '').replace(',', '.').strip())
    return x

def main():
    # Caminho do arquivo relativo ao script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjusted paths based on project structure
    file_path = os.path.join(script_dir, '..', 'scripts', 'contas.csv')
    dict_path = os.path.join(script_dir, '..', 'scripts', 'dicionario_secretarias.csv')
    
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return

    # Carregar dados
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # Carregar dicionário de secretarias
    try:
        if os.path.exists(dict_path):
            df_dict = pd.read_csv(dict_path)
            # Merge para trazer a Área de Atuação
            # Assumindo que 'Secretaria' no contas.csv corresponde a 'Sigla' no dicionario
            # Mas contas.csv pode ter múltiplas secretarias separadas por vírgula.
            # Simplificação: Vamos pegar a primeira secretaria listada se houver mais de uma para classificação
            
            # Função para pegar a primeira secretaria limpa
            def get_first_dept(dept_str):
                if isinstance(dept_str, str):
                    return dept_str.split(',')[0].strip()
                return dept_str

            df['Secretaria_Principal'] = df['Secretaria'].apply(get_first_dept)
            
            df = df.merge(df_dict[['Sigla', 'Área de Atuação']], left_on='Secretaria_Principal', right_on='Sigla', how='left')
            
            # Preencher nulos com 'Outros' ou manter a Secretaria original se não encontrar
            df['Área de Atuação'] = df['Área de Atuação'].fillna('Outros')
        else:
            print(f"Aviso: Dicionário {dict_path} não encontrado. Usando 'Secretaria' como base.")
            df['Área de Atuação'] = df['Secretaria']
            
    except Exception as e:
        print(f"Erro ao carregar dicionário ou fazer merge: {e}")
        df['Área de Atuação'] = df['Secretaria']

    # Limpeza de dados
    print("Limpando dados...")
    df['Valor do Repasse'] = df['Valor do Repasse'].apply(clean_currency)
    
    # Criar diretório para salvar gráficos se não existir
    output_dir = script_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 1. Top 10 Entidades com Maior Repasse
    print("Gerando gráfico 1: Top 10 Entidades...")
    top_10 = df.nlargest(10, 'Valor do Repasse')
    plt.figure(figsize=(14, 8))
    sns.barplot(data=top_10, y='Entidade', x='Valor do Repasse', palette='viridis')
    plt.title('Top 10 Entidades com Maior Repasse')
    plt.xlabel('Valor do Repasse (R$)')
    plt.ylabel('Entidade')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '1_top_10_entidades.png'))
    plt.close()

    # 2. Distribuição de Verba por Área de Atuação
    print("Gerando gráfico 2: Distribuição por Área de Atuação (Pizza)...")
    # Usar 'Área de Atuação' em vez de 'Secretaria'
    target_col = 'Área de Atuação'
    dept_sum = df.groupby(target_col)['Valor do Repasse'].sum().sort_values(ascending=False)
    
    # Agrupar fatias muito pequenas (< 2%) em "Outros" para evitar sobreposição
    # REMOVIDO A PEDIDO DO USUÁRIO: Mostrar todas as áreas
    # total_repasse = dept_sum.sum()
    # threshold = 0.02 * total_repasse
    
    # large_slices = dept_sum[dept_sum >= threshold].copy()
    # small_slices = dept_sum[dept_sum < threshold]
    
    # if not small_slices.empty:
    #     if 'Outros' in large_slices:
    #          large_slices['Outros'] += small_slices.sum()
    #     else:
    #          large_slices['Outros'] = small_slices.sum()
    #     dept_sum = large_slices

    
    plt.figure(figsize=(16, 10))
    # Usar uma paleta com cores suficientes
    colors = sns.color_palette('Set3', len(dept_sum))
    
    total_val = dept_sum.sum()

    def format_autopct(pct):
        return f'{pct:.1f}%' if pct > 2 else ''

    wedges, texts, autotexts = plt.pie(dept_sum, labels=None, autopct=format_autopct, startangle=140, colors=colors, pctdistance=0.85)
    
    # Criar legendas detalhadas
    legend_labels = []
    for label, value in zip(dept_sum.index, dept_sum.values):
        pct = (value / total_val) * 100
        val_str = f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        legend_labels.append(f'{label}: {val_str} ({pct:.1f}%)')

    plt.legend(wedges, legend_labels, title=f"{target_col}", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    total_val_str = f'R$ {total_val:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    plt.title(f'Distribuição de Verba por {target_col}\nTotal: {total_val_str}', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_distribuicao_area_atuacao.png'), bbox_inches='tight')
    plt.close()

    # Gerar relatório de texto detalhado
    report_path = os.path.join(output_dir, '2_distribuicao_area_atuacao_detalhado.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"=== Relatório Detalhado: Distribuição de Verba por {target_col} ===\n\n")
        f.write(f"Valor Total Repassado: {total_val_str}\n\n")
        f.write("Detalhamento por Área:\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Área de Atuação':<50} | {'Valor (R$)':<20} | {'%':<10}\n")
        f.write("-" * 80 + "\n")
        
        for label, value in zip(dept_sum.index, dept_sum.values):
            pct = (value / total_val) * 100
            val_str = f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
            f.write(f"{label:<50} | {val_str:<20} | {pct:>6.2f}%\n")
            
        f.write("-" * 80 + "\n")
    
    print(f"Relatório detalhado salvo em: {report_path}")

    # 2.1 Bar Chart by Area
    print(f"Gerando gráfico 2.1: Barras por {target_col}...")
    plt.figure(figsize=(14, 8))
    sns.barplot(x=dept_sum.index, y=dept_sum.values, palette='viridis')
    plt.title(f'Distribuição de Verba por {target_col}\nTotal: {total_val_str}', fontsize=14)
    plt.xlabel(target_col)
    plt.ylabel('Valor Total (R$)')
    plt.xticks(rotation=45, ha='right')
    
    # Adicionar rótulos de valor nas barras
    for i, v in enumerate(dept_sum.values):
        val_str = f'R$ {v:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        plt.text(i, v, val_str, ha='center', va='bottom', fontsize=9)
        
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_1_barras_area_atuacao.png'))
    plt.close()

    # 3. Histograma de Valores
    print("Gerando gráfico 3: Histograma de Valores...")
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Valor do Repasse'], bins=30, kde=True)
    plt.title('Distribuição dos Valores de Repasse')
    plt.xlabel('Valor do Repasse (R$)')
    plt.ylabel('Frequência')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '3_histograma_valores.png'))
    plt.close()

    # 4. Análise de Pareto
    print("Gerando gráfico 4: Análise de Pareto...")
    df_sorted = df.sort_values(by='Valor do Repasse', ascending=False)
    df_sorted['Acumulado'] = df_sorted['Valor do Repasse'].cumsum()
    df_sorted['Percentual Acumulado'] = 100 * df_sorted['Acumulado'] / df_sorted['Valor do Repasse'].sum()
    
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Gráfico de barras
    ax1.bar(range(len(df_sorted)), df_sorted['Valor do Repasse'], color='C0')
    ax1.set_ylabel('Valor do Repasse (R$)', color='C0')
    ax1.tick_params(axis='y', labelcolor='C0')
    ax1.set_xlabel('Entidades (Ordenadas por Valor)')
    
    # Linha de acumulado
    ax2 = ax1.twinx()
    ax2.plot(range(len(df_sorted)), df_sorted['Percentual Acumulado'], color='C1', marker='D', ms=2)
    ax2.set_ylabel('Percentual Acumulado (%)', color='C1')
    ax2.tick_params(axis='y', labelcolor='C1')
    ax2.axhline(80, color='grey', linestyle='--')
    
    plt.title('Análise de Pareto dos Repasses')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '4_pareto.png'))
    plt.close()

    # 5. Nuvem de Palavras
    print("Gerando gráfico 5: Nuvem de Palavras...")
    text = ' '.join(df['Entidade'].astype(str))
    # Remover palavras comuns irrelevantes para a nuvem se necessário
    stopwords = ['DE', 'DA', 'DO', 'DOS', 'DAS', 'E', 'A', 'O', 'EM', 'PARA', 'COM', 'POR', 'SANTOS', 'ASSOCIAÇÃO', 'SOCIEDADE', 'INSTITUTO', 'CENTRO', 'GRUPO', 'GRÊMIO', 'APM', 'UME']
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Nuvem de Palavras dos Nomes das Entidades')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_nuvem_palavras.png'))
    plt.close()

    # 6. Gráfico de Barras dos Totais por Secretaria (Apenas Valores)
    print("Gerando gráfico 6: Totais por Secretaria (Barras)...")
    plt.figure(figsize=(12, 8))
    # Recalcular sem o agrupamento "Outros" para ver todas
    dept_sum_all = df.groupby('Secretaria')['Valor do Repasse'].sum().sort_values(ascending=False)
    sns.barplot(x=dept_sum_all.index, y=dept_sum_all.values, palette='viridis')
    plt.title('Total de Repasses por Secretaria')
    plt.xlabel('Secretaria')
    plt.ylabel('Valor Total (R$)')
    plt.xticks(rotation=45)
    
    # Adicionar rótulos de valor nas barras
    for i, v in enumerate(dept_sum_all.values):
        plt.text(i, v, f'R$ {v:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.'), 
                 ha='center', va='bottom')
                 
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '6_total_secretaria_barras.png'))
    plt.close()

    print("Concluído! Gráficos salvos na pasta 'analises/'.")

if __name__ == "__main__":
    main()
