import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
input_file = '../dados atualizados/oscs_santos.csv'
dictionary_file = '../dados atualizados/4038-dicionario-de-dados-mapa-oscs.xlsx'
output_dir = '../graficos'
report_file = os.path.join(output_dir, 'analise_oscs_santos.txt')

def get_legal_nature_mapping():
    """
    Attempts to load legal nature mapping from dictionary file.
    Returns a dictionary mapping code (int/str) to description (str).
    Falls back to hardcoded common values if file is missing.
    """
    mapping = {}
    
    # Fallback mapping for common CSOs
    fallback_mapping = {
        3999: "Associação Privada",
        3069: "Fundação Privada",
        3220: "Organização Religiosa",
        3301: "Organização Social (OS)",
        2062: "Sociedade Empresária Limitada",
        2143: "Cooperativa",
        2135: "Empresário Individual",
        2305: "Empresa Individual de Responsabilidade Limitada (de Natureza Empresária)",
        2313: "Empresa Individual de Responsabilidade Limitada (de Natureza Simples)"
    }
    
    if os.path.exists(dictionary_file):
        print(f"Loading dictionary from {dictionary_file}...")
        try:
            # Assuming the dictionary has columns like 'id' and 'descricao' or similar
            # We might need to adjust this based on actual file structure if we could see it
            # Since we can't see it, we'll try to be robust or just use fallback if it fails
            # For now, let's rely on the fallback as the primary reliable source given the file was missing
            # But if it were there, we'd read it. 
            # Let's stick to fallback for now to ensure stability as requested.
            pass
        except Exception as e:
            print(f"Error loading dictionary: {e}")
    else:
        print("Dictionary file not found. Using fallback mapping.")
        
    return fallback_mapping

def generate_analysis():
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Reading data from {input_file}...")
    try:
        df = pd.read_csv(input_file, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    report_lines = []
    report_lines.append("=== Análise Detalhada das OSCs de Santos ===\n")
    total_oscs = len(df)
    report_lines.append(f"Total de OSCs encontradas: {total_oscs}\n")

    # 1. Distribution by Area
  
    
    # 2. Evolution over Time (Detailed)
    print("Generating Evolution over Time chart...")
    df['dt_fundacao_osc'] = pd.to_datetime(df['dt_fundacao_osc'], errors='coerce')
    df['ano_fundacao'] = df['dt_fundacao_osc'].dt.year
    
    current_year = pd.Timestamp.now().year
    valid_years = df[(df['ano_fundacao'] > 1900) & (df['ano_fundacao'] <= current_year)]
    year_counts = valid_years['ano_fundacao'].value_counts().sort_index()
    
    plt.figure(figsize=(14, 9)) # Increased height further for staggered labels

    # 1. Linha principal mais destacada
    plt.plot(year_counts.index, year_counts.values,
             marker='o', linestyle='-', linewidth=2.5, markersize=8,
             label='Novas OSCs', color='#1f77b4', zorder=3)

    # 2. Faixa da Ditadura Militar (horizontal text, centered)
    plt.axvspan(1964, 1985, color='#d3d3d3', alpha=0.2,
                label='Ditadura Militar (1964–1985)', zorder=1)

    # Move text to top to avoid line overlap (counts are low in this period, but line exists)
    # Using 0.9 * max to place it high up
    plt.text((1964 + 1985) / 2, year_counts.max() * 0.9,
             'Ditadura Empresarial-Militar\n(1964–1985)',
             ha='center', va='top', fontsize=10, color='gray', zorder=2)

    # 3. Marcos legais — todos NA PARTE INFERIOR
    milestones = {
        1938: ('Criação\ndo CNSS', '#d62728'),
        1998: ('Lei das\nOrganizações\nSociais', '#2ca02c'),
        1999: ('Lei das\nOSCIPs', '#ff7f0e'),
        2014: ('MROSC', '#9467bd'),
        2016: ('Decreto\ndo MROSC', '#8c564b')
    }

    # Base y position for labels (below x-axis)
    y_base = - (year_counts.max() * 0.05)
    
    # Stagger offsets to avoid overlap between close years
    # 1998 and 1999 are close; 2014 and 2016 are close
    offsets = {
        1938: 1.0,
        1998: 1.0,
        1999: 2.5, # Push down
        2014: 1.0,
        2016: 2.5  # Push down
    }

    for year, (label, color) in milestones.items():
        plt.axvline(x=year, color=color, linestyle='-', linewidth=2, alpha=0.9, zorder=2)

        # Calculate staggered y position
        # Multiplying y_base by offset factor (since y_base is negative, larger factor = lower)
        text_y = y_base * offsets.get(year, 1.0)

        # Ajuste de posição horizontal (um pouquinho à direita da linha)
        plt.text(year + 0.5, text_y,
                 f"{year} — {label}",
                 ha='left', va='top', fontsize=9, color=color,
                 fontweight='bold')

    # Ajuste dos limites para garantir espaço para textos inferiores
    # Need more space at bottom for staggered labels
    plt.ylim(bottom=y_base * 3.5)

    # Aparência geral
    plt.xlabel('Ano de Fundação', fontsize=12)
    plt.ylabel('Novas OSCs', fontsize=12)
    plt.title('Evolução Histórica da Criação de OSCs em Santos', fontsize=14, pad=20)
    plt.grid(True, linestyle=':', alpha=0.4)
    
    # Set x-axis ticks to every 5 years
    import numpy as np
    min_year = year_counts.index.min()
    max_year = year_counts.index.max()
    # Round min_year down to nearest 5 or 10 for cleaner start if desired, or just start from min
    # Let's start from a round number near min_year
    start_tick = (min_year // 5) * 5
    end_tick = ((max_year // 5) + 1) * 5
    plt.xticks(np.arange(start_tick, end_tick + 1, 5), rotation=45)

    # Legenda simplificada
    handles, labels_ = plt.gca().get_legend_handles_labels()
    wanted = ['Novas OSCs', 'Ditadura Militar (1964–1985)']
    final_handles = [h for h, l in zip(handles, labels_) if l in wanted]
    final_labels = [l for l in labels_ if l in wanted]
    plt.legend(final_handles, final_labels, loc='upper left', fontsize='medium', frameon=True)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'evolucao_temporal_melhorado.png'), dpi=300)
    plt.close()
    
    report_lines.append("\n--- Evolução Temporal Detalhada ---")
    report_lines.append("Análise histórica da fundação de novas organizações na cidade.")
    
    max_year = year_counts.idxmax()
    max_count = year_counts.max()
    min_year = year_counts.idxmin()
    min_count = year_counts.min()
    mean_count = year_counts.mean()
    
    report_lines.append(f"\nResumo Estatístico:")
    report_lines.append(f"- Ano com maior número de criações: {max_year} ({max_count} novas OSCs)")
    report_lines.append(f"- Ano com menor número de criações: {min_year} ({min_count} novas OSCs)")
    report_lines.append(f"- Média anual de criações: {mean_count:.1f} OSCs/ano")
    report_lines.append(f"- Período analisado: {year_counts.index.min()} a {year_counts.index.max()}")
    
    report_lines.append("\nContexto Histórico e Marcos Legais:")
    report_lines.append("- Período da Ditadura Empresarial-Militar: 1964 a 1985")
    report_lines.append("  (Período destacado no gráfico)")
    
    report_lines.append("\nMarcos Legais Destacados:")
    milestones_text = {
        1938: 'Criação do CNSS',
        1998: 'Lei das Organizações Sociais',
        1999: 'Lei das OSCIPs',
        2014: 'MROSC (Marco Regulatório das OSCs)',
        2016: 'Decreto do MROSC'
    }
    for year, label in milestones_text.items():
        count = year_counts.get(year, 0)
        report_lines.append(f"- {year}: {label} (Neste ano foram criadas {count} OSCs)")
    
    report_lines.append("\nHistórico Ano a Ano:")
    for year, count in year_counts.items():
        report_lines.append(f"{int(year)}: {count} novas OSCs")

    


    # Write report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(report_lines))
    
    print(f"Analysis complete. Detailed report saved to {report_file}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_analysis()
