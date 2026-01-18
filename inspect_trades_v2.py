
import zipfile
import io

filename = "trades_202510.zip"

with open(filename, "rb") as f:
    zip_bytes = f.read()

with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
    for name in z.namelist():
        print(f"FILE: {name}")
        with z.open(name) as f_in:
            head = f_in.read(4096).decode('latin-1', errors='replace')
            lines = head.splitlines()
            for i, line in enumerate(lines[:15]):
                print(f"L{i}: {line}")
