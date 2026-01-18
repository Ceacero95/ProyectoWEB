
import pandas as pd
import io

raw_csv_content = """Fecha;Contrato;Agente compra;Unidad compra;Zona compra;Agente venta;Unidad venta;Zona venta;Precio;Cantidad;Momento casación;
01/10/2025;20251001 00:00-20251001 00:15;GRTEN;GRTEC01;10YES-REE------0;;;;104,01;0,50;30/09/2025 22:22:29;
01/10/2025;20251001 07:00-20251001 07:15;TAUTR;TAURM01;10YES-REE------0;GRTEN;GRTEC01;10YES-REE------0;111,41;0,10;30/09/2025 22:24:02;"""

def test_parsing():
    print("--- RAW CONTENT ---")
    print(raw_csv_content)
    
    df = pd.read_csv(io.StringIO(raw_csv_content), sep=';', on_bad_lines='skip')
    
    print("\n--- ORIGINAL COLUMNS ---")
    print(df.columns.tolist())
    
    # Normalize
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    print("\n--- NORMALIZED COLUMNS ---")
    print(df.columns.tolist())
    
    print("\n--- DATAFRAME HEAD ---")
    print(df.head())
    
    target_cols = ['agente_compra', 'unidad_compra']
    for c in target_cols:
        if c in df.columns:
            print(f"\nCol '{c}' First Row Value: '{df[c].iloc[0]}'")
            print(f"Col '{c}' Type: {df[c].dtype}")
        else:
            print(f"\nCol '{c}' NOT FOUND")

if __name__ == "__main__":
    test_parsing()
