import os
import requests
from tqdm import tqdm

# Código da estação SCRM (WMO ID + WBAN)
wmo_id = '89062'
wban_id = '99999'  # WBAN inexistente, mas usado como placeholder
station_code = f'{wmo_id}-{wban_id}'

# Diretório de saída
output_dir = 'dados_metar_scrm'
os.makedirs(output_dir, exist_ok=True)

# Período de interesse
anos = range(2016, 2024)

base_url = 'https://www.ncei.noaa.gov/data/global-hourly/access'

for ano in anos:
    file_url = f"{base_url}/{ano}/{station_code}.csv"
    local_path = os.path.join(output_dir, f"{station_code}_{ano}.csv")

    try:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(1024), desc=f"Baixando {ano}"):
                    f.write(chunk)
        else:
            print(f"[{ano}] Arquivo não encontrado: {file_url}")
    except Exception as e:
        print(f"Erro no download de {ano}: {e}")
