import pandas as pd
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'contas.csv')
    
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return

    df = pd.read_csv(file_path)

    # Mapeamento de atualizações: "Parte do Nome" -> ("Novo Valor", "Nova Secretaria")
    updates = {
        "UACEP - UNIÃO DE AMPARO": ("R$ 247.500,00", "SEMULHER"),
        "INSTITUTO DEVIR EDUCOM": ("R$ 262.189,75", "SEMULHER"),
        "CONCIDADANIA": ("R$ 524.764,00", "SEMULHER"),
        "BAIRRO DA POMPEIA": ("R$ 31.200,00", "SEMULHER"),
        "AMIGOS DO SÃO BENTO": ("R$ 31.200,00", "SEMULHER"),
        "BAIRRO DA ENCRUZILHADA": ("R$ 50.700,00", "SEMULHER"),
        "VILA BELMIRO": ("R$ 31.200,00", "SEMULHER"),
        "JARDIM BOM RETIRO": ("R$ 31.200,00", "SEMULHER"),
        "MORRO DO JOSÉ MENINO": ("R$ 31.200,00", "SEMULHER"),
        "COSTA E SILVA": ("R$ 31.200,00", "SEMULHER"),
        "BAIRRO DO MARAPÉ": ("R$ 31.200,00", "SEMULHER"),
        "CANELEIRA III": ("R$ 31.200,00", "SEMULHER"),
        "PRÓ-MELHORAMENTOS DO BAIRRO DA CANELEIRA": ("R$ 31.200,00", "SEMULHER"),
        "MORRO DA NOVA CINTRA": ("R$ 31.200,00", "SEMULHER"),
        "VILA SÃO JORGE": ("R$ 31.200,00", "SEMULHER"),
        "VILA ALEMOA": ("R$ 31.200,00", "SEMULHER"),
        "JARDIM SÃO MANOEL": ("R$ 31.200,00", "SEMULHER"),
        "JARDIM CASTELO": ("R$ 27.300,00", "SEMULHER"),
        "MOVIMENTO DE ARREGIMENTAÇÃO FEMININA": ("R$ 20.000,00", "SEMULHER"),
        "NINHO DE AMOR E LUZ": ("R$ 97.565,00", "SEMULHER"),
        "COT - CENTRO ORGANIZATIVO": ("R$ 337.714,13", "SEMULHER"),
        "VILA PANTANAL": ("R$ 15.000,00", "SEMULHER"),
        "BAIRRO DO CAMPO GRANDE": ("R$ 7.800,00", "SEMULHER"),
        "CAMINHO DE SANTA MARIA": ("R$ 11.700,00", "SEMULHER"),
        "PRÓ MORADIA ILHÉUS": ("R$ 23.400,00", "SEMULHER"),
        "AFROSAN": ("R$ 11.000,00", "SEMULHER"),
        "BAIRRO DO CARUARA": ("R$ 23.400,00", "SEMULHER"),
        "CASTELO BRANCO": ("R$ 31.200,00", "SEMULHER"),
        "QUILOA": ("R$ 0,00", "SEMULHER"),
        "MORRO DO PACHECO": ("R$ 27.300,00", "SEMULHER"),
        "PARADA DO ORGULHO": ("R$ 76.710,00", "SEMULHER"),
        "JARDIM PIRATININGA": ("R$ 27.300,00", "SEMULHER"),
        "MONTE SERRAT": ("R$ 15.600,00", "SEMULHER"),
        "DO EMBARÉ": ("R$ 23.400,00", "SEMULHER"),
        "NOSSA SENHORA DA CONCEIÇÃO": ("R$ 81.000,00", "SEMULHER"),
        "PROCOMUM": ("R$ 11.000,00", "SEMULHER"),
        "ABRASOFFA": ("R$ 40.000,00", "SEMULHER"),
        "ORDEM FRANCISCANA": ("R$ 10.800,00", "SEMULHER"),
        "VILA MATHIAS": ("R$ 15.600,00", "SEMULHER"),
        "JABAQUARA": ("R$ 11.700,00", "SEMULHER"),
        "MULTIVERSO": ("R$ 20.000,00", "SEMULHER"),
        "BAIRRO MACUCO": ("R$ 27.300,00", "SEMULHER"),
    }

    count = 0
    for key, (val, dept) in updates.items():
        # Encontrar índices que contêm a chave no nome da entidade
        mask = df['Entidade'].str.contains(key, case=False, regex=False)
        if mask.any():
            df.loc[mask, 'Valor do Repasse'] = val
            df.loc[mask, 'Secretaria'] = dept
            count += mask.sum()
            print(f"Atualizado: {key} -> {dept}, {val}")
        else:
            print(f"AVISO: Não encontrado: {key}")

    print(f"Total de registros atualizados: {count}")
    
    df.to_csv(file_path, index=False, quoting=1)

if __name__ == "__main__":
    main()
