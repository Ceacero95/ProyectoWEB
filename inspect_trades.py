
import zipfile
import io

filename = "trades_202510.zip"

with open(filename, "rb") as f:
    zip_bytes = f.read()

with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
    print("Files in ZIP:", z.namelist())
    for name in z.namelist():
        if name.endswith('.txt') or name.endswith('.1'): # Assuming it might be .1 like others or .txt
            print(f"\n--- Content of {name} (First 10 lines) ---")
            with z.open(name) as f_in:
                # Read a bit
                head = f_in.read(2048).decode('latin-1', errors='replace')
                print('\n'.join(head.splitlines()[:10]))
