import pandas as pd
import re
from metar.Metar import Metar

# === CONFIGURAÇÃO ===
CAMINHO_CSV = "scrm_metars_2015_2025.csv"
CAMINHO_SAIDA = "scrm_metar_decodificado.csv"

# === FUNÇÕES AUXILIARES ===

def extrair_fenomenos(metar_str):
    """Extrai fenômenos do código METAR com regex."""
    fenomenos = {
        'rain_light': bool(re.search(r'\-RA\b', metar_str)),
        'rain_moderate': bool(re.search(r'(?<!\+|\-|\w)RA\b', metar_str)),
        'rain_heavy': bool(re.search(r'\+RA\b', metar_str)),
        'snow': bool(re.search(r'\bSN\b', metar_str)),
        'fog': bool(re.search(r'\bFG\b', metar_str)),
        'mist': bool(re.search(r'\bBR\b', metar_str)),
        'drizzle': bool(re.search(r'\bDZ\b', metar_str)),
        'thunderstorm': bool(re.search(r'\bTS\b', metar_str)),
        'showers': bool(re.search(r'\bSH\b', metar_str)),
        'haze': bool(re.search(r'\bHZ\b', metar_str)),
    }
    fenomenos["weather_raw"] = ", ".join([k for k, v in fenomenos.items() if v])
    return fenomenos

# === LEITURA DO ARQUIVO ===
df_raw = pd.read_csv(CAMINHO_CSV)

# === DECODIFICAÇÃO ===
dados = []
for i, row in df_raw.iterrows():
    metar_str = row["metar"].strip()
    try:
        metar = Metar(metar_str)

        registro = {
            "datetime": pd.to_datetime(row["valid"]),
            "temperature_C": metar.temp.value() if metar.temp else None,
            "dewpoint_C": metar.dewpt.value() if metar.dewpt else None,
            "wind_dir_deg": metar.wind_dir.value() if metar.wind_dir else None,
            "wind_speed_kt": metar.wind_speed.value() if metar.wind_speed else None,
            "wind_gust_kt": metar.wind_gust.value() if metar.wind_gust else None,
            "visibility_m": metar.vis.value() if metar.vis else None,
            "pressure_hPa": metar.press.value() if metar.press else None,
        }

        # Adicionar fenômenos
        fenomenos = extrair_fenomenos(metar_str)
        registro.update(fenomenos)

        dados.append(registro)

    except Exception as e:
        print(f"❌ Erro ao decodificar linha {i}: {e}")

# === SALVAR RESULTADO ===
df_final = pd.DataFrame(dados)
df_final.to_csv(CAMINHO_SAIDA, index=False)
print(f"✅ Arquivo salvo: {CAMINHO_SAIDA}")
