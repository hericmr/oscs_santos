import pandas as pd
import os

import zipfile
import shutil

# Configuration
SANTOS_OSCS_PATH = 'dashboard_oscs/data/oscs_santos.csv'
DATA_DIR = 'dados atualizados'
OUTPUT_DIR = os.path.join(DATA_DIR, 'dados_filtrados')
TEMP_DIR = os.path.join(DATA_DIR, 'temp_zip_extract')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_santos_cnpjs():
    """Loads the list of CNPJs from the Santos OSCs file."""
    print(f"Loading Santos OSCs from {SANTOS_OSCS_PATH}...")
    try:
        df = pd.read_csv(SANTOS_OSCS_PATH, sep=';', dtype={'cnpj': str})
        # Clean CNPJ: remove non-numeric characters if any (though likely clean)
        df['cnpj_clean'] = df['cnpj'].str.replace(r'\D', '', regex=True)
        cnpjs = set(df['cnpj_clean'].unique())
        print(f"Loaded {len(cnpjs)} unique CNPJs.")
        return cnpjs
    except Exception as e:
        print(f"Error loading Santos OSCs: {e}")
        return set()

def filter_file(file_path, santos_cnpjs):
    """Filters a single file based on CNPJ/ID match."""
    filename = os.path.basename(file_path)
    print(f"\nProcessing {filename}...")
    
    # Determine the key column and separator based on filename or inspection
    # Based on previous analysis:
    key_col = None
    sep = ',' # Default for CSV, but many here are ;
    
    if filename.endswith('.csv'):
        # Just a guess, might need refinement if more CSVs appear
        sep = ';' 
    
    # Mapping based on headers.txt analysis & re-inspection
    header_row = 0
    if 'area_subarea' in filename or 'baseprojetososcantiga' in filename:
        key_col = 'cd_identificador_osc'
    elif 'recursososc' in filename:
        key_col = 'cd_identificador_osc' # Verifying this assumptions
    elif '1434-cebassaude' in filename:
        key_col = 'NU_CNPJ'
    elif '8420-cebaseducacao' in filename:
        key_col = 'CNPJ'
    elif '7684-cebassuas' in filename:
        header_row = 4 # Skip first 4 rows
        key_col = 'CNPJ' # Likely CNPJ column exists
    elif 'oscs_santos' in filename:
        print("Skipping source file.")
        return 
    
    # Attempt to read
    try:
        if filename.endswith('.csv'):
            # Try efficient reading with common params first, then fallback
            encodings = ['utf-8', 'latin1', 'cp1252']
            separators = [sep, '\t', ',', ';'] # separators to try if default fails or if specialized logic needed
            
            df = None
            last_error = None
            
            for encoding in encodings:
                for separator in separators:
                    try:
                        # Skip bad lines to avoid crash, but maybe wanr?
                        # on_bad_lines='skip' might hide issues, but for bulk processing typical in gov data...
                        df = pd.read_csv(file_path, sep=separator, dtype=str, header=header_row, encoding=encoding, on_bad_lines='warn')
                        
                        # Validate columns - check if we have > 1 column or if the key is present
                        # If we read 1 column but expected more, maybe wrong separator
                        if len(df.columns) > 1:
                            # Also check if we found a potential key?
                            # Let's assume valid if > 1 col for now, or check key later
                            break 
                        else:
                            df = None # Reset if 1 column (suspicious for these files)
                    except Exception as e:
                        last_error = e
                        continue
                if df is not None:
                    print(f"Read {filename} with encoding={encoding}, sep={repr(separator)}")
                    break
            
            if df is None:
                raise Exception(f"Failed to read CSV with tried encodings/separators. Last error: {last_error}")

        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path, dtype=str, header=header_row)
        elif filename.endswith('.xls'):
             df = pd.read_excel(file_path, dtype=str, engine='xlrd', header=header_row)
        else:
            print(f"Skipping unsupported file type: {filename}")
            return

        # Normalize columns to find key if not explicitly mapped
        if key_col is None:
            # excessive search
            possible_keys = ['cnpj', 'nu_cnpj', 'cd_identificador_osc', 'id_osc']
            for col in df.columns:
                if col.lower() in possible_keys:
                    key_col = col
                    break
        
        if key_col and key_col in df.columns:
            print(f"Found key column: {key_col}")
            # Normalize key column
            df['key_clean'] = df[key_col].astype(str).str.replace(r'\D', '', regex=True)
            
            # Filter
            initial_count = len(df)
            filtered_df = df[df['key_clean'].isin(santos_cnpjs)].copy()
            final_count = len(filtered_df)
            
            print(f"Rows: {initial_count} -> {final_count}")
            
            if final_count > 0:
                # Drop helper column
                filtered_df.drop(columns=['key_clean'], inplace=True)
                
                # Save
                output_path = os.path.join(OUTPUT_DIR, filename)
                # Save as CSV for consistency and speed, or keep original format?
                # Let's save as CSV to avoid excel writer issues and for easier usage later, 
                # unless it was an excel file, then maybe keep it?
                # Actually, CSV is safer for data portability.
                output_csv_path = os.path.splitext(output_path)[0] + '.csv'
                filtered_df.to_csv(output_csv_path, index=False, sep=';')
                print(f"Saved filtered data to {output_csv_path}")
            else:
                print("No matching records found.")
        else:
            print(f"Could not identify key column in {filename}. Columns: {df.columns.tolist()}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

def process_zip(zip_path, santos_cnpjs):
    """Extracts zip and processes contained CSVs."""
    print(f"\nProcessing zip archive: {zip_path}")
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_DIR)
            
        # Walk through extracted files
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                if file.endswith('.csv') or file.endswith('.xlsx') or file.endswith('.xls'):
                    full_path = os.path.join(root, file)
                    filter_file(full_path, santos_cnpjs)
                    
        # Cleanup
        shutil.rmtree(TEMP_DIR)
    except Exception as e:
        print(f"Error processing zip {zip_path}: {e}")

def main():
    santos_cnpjs = load_santos_cnpjs()
    if not santos_cnpjs:
        print("No Santos CNPJs found. Aborting.")
        return

    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        if filename.endswith('.zip'):
             process_zip(file_path, santos_cnpjs)
        elif os.path.isfile(file_path):
            filter_file(file_path, santos_cnpjs)

if __name__ == "__main__":
    main()
