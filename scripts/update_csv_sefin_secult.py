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
        "CAMPS - CENTRO DE APRENDIZAGEM": ("R$ 5.371.489,10", "SEFIN"),
        "BANDA MUSICAL CARLOS GOMES": ("R$ 57.955,92", "SECULT"),
        "IHGS - INSTITUTO HISTÓRICO": ("R$ 282.855,00", "SECULT"),
        "ABRACE - ASSOCIAÇÃO BRASILEIRA": ("R$ 716.448,00", "SECULT"),
        "INSTITUTO ARTE NO DIQUE": ("R$ 975.704,00", "SECULT"),
        "ASSOCIAÇÃO BALÉ DA CIDADE": ("R$ 747.000,00", "SECULT"),
        "ASSOCIAÇÃO IN PHOCCUS": ("R$ 452.125,20", "SECULT"),
        "FUNDAÇÃO PINACOTECA BENEDICTO": ("R$ 608.000,00", "SECULT"),
        "MUSEU DE ARTE SACRA": ("R$ 120.000,00", "SECULT"),
        "ASSOCIAÇÃO PROJETO TAMTAM": ("R$ 515.000,00", "SECULT"),
        "MOCIDADE AMAZONENSE": ("R$ 0,00", "SECULT"),
        "FUNDAÇÃO SETTAPORT": ("R$ 31.000,00", "SECULT"),
        "ASSOCIAÇÃO CANAL CULTURAL": ("R$ 354.565,00", "SECULT"),
        "VILA MATHIAS": ("R$ 19.328,00", "SECULT"),
        "PORTO CIRCENSE": ("R$ 227.710,00", "SECULT"),
        "CONCIDADANIA": ("R$ 14.770,00", "SECULT"),
        "VILA DO TEATRO": ("R$ 14.940,00", "SECULT"),
        "PRÓTRABALHADOR": ("R$ 200.000,00", "SECULT"),
        "ASSOCIAÇÃO CULTURAL QUILOA": ("R$ 122.650,00", "SECULT"),
        "IMPÉRIO DA VILA": ("R$ 123.000,00", "SECULT"),
        "SOCIEDADE HUMANITÁRIA DOS EMPREGADOS": ("R$ 15.000,00", "SECULT"),
        "NINHO DE AMOR E LUZ": ("R$ 35.000,00", "SECULT"),
        "AMIGOS DO SÃO BENTO": ("R$ 10.990,00", "SECULT"),
        "PADRE PAULO": ("R$ 162.500,00", "SECULT"),
        "BANDA FAMÍLIA DO BEM": ("R$ 50.000,00", "SECULT"),
        "UNIÃO IMPERIAL": ("R$ 216.000,00", "SECULT"),
        "BANDEIRANTES DO SABOÓ": ("R$ 216.000,00", "SECULT"),
        "MOCIDADE INDEPENDÊNCIA": ("R$ 216.000,00", "SECULT"),
        "SAMBA BRASIL": ("R$ 108.000,00", "SECULT"),
        "CAMISA ALVINEGRA": ("R$ 108.000,00", "SECULT"),
        "DRAGOES DO CASTELO": ("R$ 108.000,00", "SECULT"),
        "REAL MOCIDADE SANTISTA": ("R$ 216.000,00", "SECULT"),
        "UNIDOS DA ZONA NOROESTE": ("R$ 148.000,00", "SECULT"),
        "UNIDOS DOS MORROS": ("R$ 216.000,00", "SECULT"),
        "ICEL": ("R$ 30.000,00", "SECULT"),
        "JOSÉ MARTÍ": ("R$ 28.000,00", "SECULT"),
        "APLAUSO CONTEMPORÂNEO": ("R$ 75.500,00", "SECULT"),
        "PARADA DO ORGULHO": ("R$ 240.610,00", "SECULT"),
        "FÁBRICA DE SOLIDARIEDADE": ("R$ 47.855,00", "SECULT"),
        "CAPOEIRA SENZALA": ("R$ 26.000,00", "SECULT"),
        "CLUBE DO CHORO": ("R$ 307.400,00", "SECULT"),
        "ASSOCIAÇÃO DOS ARTISTAS": ("R$ 10.855,00", "SECULT"),
        "EXPRESSÃO DE VIDA": ("R$ 45.000,00", "SECULT"),
        "ACADEMIA SANTISTA DE LETRAS": ("R$ 36.000,00", "SECULT"),
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
    
    df.to_csv(file_path, index=False, quoting=1) # quoting=1 ensures quotes around strings

if __name__ == "__main__":
    main()
