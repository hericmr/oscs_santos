import pandas as pd
import os

try:
    df = pd.read_csv('dashboard_oscs/data/oscs_santos.csv', sep=';', encoding='utf-8')
except:
    df = pd.read_csv('dashboard_oscs/data/oscs_santos.csv', sep=',', encoding='utf-8')

print("Columns:", list(df.columns))

# Check for keywords in columns
keywords = ['oscip', 'titul', 'certif', 'qualif']
possible_cols = [c for c in df.columns if any(k in c.lower() for k in keywords)]
print("Possible OSCIP columns:", possible_cols)

# Check content
if 'tx_razao_social_osc' in df.columns:
    oscip_in_name = df[df['tx_razao_social_osc'].str.contains('OSCIP', case=False, na=False)]
    print(f"Rows with OSCIP in name: {len(oscip_in_name)}")
    
if 'tx_nome_fantasia_osc' in df.columns:
    oscip_in_fantasy = df[df['tx_nome_fantasia_osc'].str.contains('OSCIP', case=False, na=False)]
    print(f"Rows with OSCIP in fantasy name: {len(oscip_in_fantasy)}")
