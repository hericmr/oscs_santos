import pandas as pd
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'contas.csv')
    
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return

    df = pd.read_csv(file_path)

    # Lista de atualizações SEMAM
    updates = [
        {"key": "ONG PATINHAS QUE BRILHAM", "val": "R$ 186.678,00", "dept": "SEMAM"},
        {"key": "INSTITUTO ARTE NO DIQUE", "val": "R$ 519.610,00", "dept": "SEMAM"},
        {"key": "INSTITUTO INOVARE", "val": "R$ 111.000,00", "dept": "SEMAM"},
        {"key": "ONG AMIGOS DO TOBÍAS", "val": "R$ 37.491,67", "dept": "SEMAM"},
        {"key": "ONG VIVA BICHO", "val": "R$ 0,00", "dept": "SEMAM"},
        {"key": "INSTITUTO MAR AZUL", "val": "R$ 30.000,00", "dept": "SEMAM"},
        {"key": "ONG CASA BRANCA", "val": "R$ 74.844,89", "dept": "SEMAM"},
        {"key": "ABRASOFFA", "val": "R$ 30.000,00", "dept": "SEMAM"},
        {"key": "INSTITUTO DE ACOLHIMENTO", "val": "R$ 100.000,00", "dept": "SEMAM"},
        {"key": "COMPOSTA & CULTIVA", "val": "R$ 20.000,00", "dept": "SEMAM"},
        {"key": "FAPUNIFESP", "val": "R$ 110.903,85", "dept": "SEMAM"},
        {"key": "INSTITUTO TAUPET", "val": "R$ 60.000,00", "dept": "SEMAM"},
        {"key": "CENTRO AMBIENTAL DE ESTUDOS", "val": "R$ 19.997,17", "dept": "SEMAM"},
        {"key": "IPAEMA", "val": "R$ 99.950,00", "dept": "SEMAM"},
    ]

    new_rows = []
    
    for item in updates:
        key = item['key']
        val = item['val']
        dept = item['dept']
        
        # Verificar se já existe essa entidade
        mask_entity = df['Entidade'].str.contains(key, case=False, regex=False)
        
        if mask_entity.any():
            # Verificar se já existe essa entidade NESTA secretaria
            mask_dept = mask_entity & (df['Secretaria'] == dept)
            
            if mask_dept.any():
                # Atualizar existente na mesma secretaria
                df.loc[mask_dept, 'Valor do Repasse'] = val
                print(f"Atualizado: {key} -> {dept}, {val}")
            else:
                # Entidade existe mas em outra secretaria -> Adicionar nova linha
                # Pegar o nome completo da entidade da primeira ocorrência encontrada
                full_name = df.loc[mask_entity, 'Entidade'].iloc[0]
                new_row = {"Entidade": full_name, "Valor do Repasse": val, "Secretaria": dept}
                new_rows.append(new_row)
                print(f"Adicionado nova linha: {full_name} -> {dept}, {val}")
        else:
            print(f"AVISO: Entidade não encontrada para atualização: {key}")

    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df = pd.concat([df, df_new], ignore_index=True)
        print(f"Total de novas linhas adicionadas: {len(new_rows)}")

    df.to_csv(file_path, index=False, quoting=1)

if __name__ == "__main__":
    main()
