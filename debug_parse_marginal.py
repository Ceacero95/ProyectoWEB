import sys
import os
import pandas as pd
import io

# Validar que existe el fichero
file_path = "local_data/bronze/omie/marginalpdbc/2026/01/marginalpdbc_20260124.1"
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    sys.exit(1)

with open(file_path, "rb") as f:
    content = f.read()

print(f"Read {len(content)} bytes.")

# Logic from src/silver/omie/marginalpdbc.py
try:
    text_content = content.decode('latin-1', errors='replace')
    print("--- CONTENT START ---")
    print(text_content[:200])
    print("--- CONTENT END ---")
    
    lines = text_content.splitlines()
    data_lines = [l for l in lines if l and l[0].isdigit()]
    
    print(f"Found {len(data_lines)} data lines.")
    
    if not data_lines:
        print("No data lines found starting with digit.")
    else:
        df = pd.read_csv(io.StringIO('\n'.join(data_lines)), sep=';', header=None)
        print("DataFrame created:")
        print(df.head())
        print("Columns:", df.columns.tolist())
        
        # Check column count logic
        expected_cols = ['anio', 'mes', 'dia', 'periodo', 'marginal_pt', 'marginal_es']
        df = df.dropna(axis=1, how='all')
        print(f"Columns after dropna: {len(df.columns)}")
        
        if len(df.columns) >= 6:
            print("Columns validation OK")
        else:
            print("Columns validation FAILED")

except Exception as e:
    print(f"Error parsing: {e}")
