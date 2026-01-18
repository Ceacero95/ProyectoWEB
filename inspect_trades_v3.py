
import zipfile
import io

filename = "trades_202510.zip"

with open(filename, "rb") as f:
    zip_bytes = f.read()

with open("inspect_out.txt", "w", encoding='utf-8') as out:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        for name in z.namelist():
            out.write(f"FILE: {name}\n")
            with z.open(name) as f_in:
                head = f_in.read(4096).decode('latin-1', errors='replace')
                lines = head.splitlines()
                for i, line in enumerate(lines[:20]):
                    out.write(f"L{i}: {line}\n")
            out.write("-" * 20 + "\n")
