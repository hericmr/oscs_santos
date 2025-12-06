import pandas as pd
import os

# Define file paths
input_file = '../dados atualizados/mapaoosc_base_dados_2025_12_11.csv'
output_file = '../dados atualizados/oscs_santos.csv'

def filter_santos_oscs():
    print(f"Reading file: {input_file}")
    
    try:
        # Read the CSV file
        # Using latin1 encoding as detected, and ';' as delimiter
        df = pd.read_csv(input_file, sep=';', encoding='latin1', low_memory=False)
        
        print("File read successfully.")
        print(f"Total rows: {len(df)}")
        
        # Filter for Santos
        # Normalizing to upper case for comparison just in case
        santos_df = df[
            (df['municipio_nome'].str.upper() == 'SANTOS') & 
            (df['UF_Sigla'].str.upper() == 'SP')
        ]
        
        print(f"Rows found for Santos: {len(santos_df)}")
        
        if len(santos_df) > 0:
            # Save to new CSV
            santos_df.to_csv(output_file, index=False, encoding='utf-8', sep=';')
            print(f"Saved filtered data to: {output_file}")
        else:
            print("No data found for Santos. Please check the city name and state.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Change working directory to the script's location to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    filter_santos_oscs()
