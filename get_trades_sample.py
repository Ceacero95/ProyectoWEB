
import os
import sys
sys.path.append(os.getcwd())
from src.common.omie_client import OmieClient

def get_sample():
    client = OmieClient()
    filename = "trades_202510.zip"
    resp = client.download_file(filename)
    if resp:
        with open(filename, 'wb') as f:
            f.write(resp.content)
        print(f"Downloaded {filename}")
    else:
        print("Failed download")

if __name__ == "__main__":
    get_sample()
