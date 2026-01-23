import requests
import csv
import os
import sys

# Add src to path
sys.path.append(os.getcwd())

from src.config.settings import ESIOS_TOKEN

def fetch_indicators():
    url = "https://api.esios.ree.es/indicators"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Token token="{ESIOS_TOKEN}"',
        "x-api-key": ESIOS_TOKEN
    }
    
    print(f"Fetching indicators from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        indicators = data.get('indicators', [])
        print(f"Found {len(indicators)} indicators.")
        
        output_file = "esios_indicators.csv"
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'short_name', 'description', 'unit_id', 'created_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            for ind in indicators:
                # Flatten description if it's a dict (sometimes localization)
                # But typically it's just a string or None
                # ESIOS API response structure check needed? Assume standard flat or dict.
                # Usually 'name' is "Precio..."
                
                row = {
                    'id': ind.get('id'),
                    'name': ind.get('name'),
                    'short_name': ind.get('short_name'),
                    'description': ind.get('description'), # Might be None
                    'unit_id': ind.get('unit_id'), # Might be relevant
                    'created_at': ind.get('created_at')
                }
                writer.writerow(row)
                
        print(f"Saved to {output_file}")
        
    except Exception as e:
        print(f"Error fetching indicators: {e}")

if __name__ == "__main__":
    fetch_indicators()
