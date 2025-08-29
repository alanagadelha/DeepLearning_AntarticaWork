# Cabeçalho do programa para retrive dos dados de METAR:
# temp: Temperatura em °C
# dwpt: Ponto de orvalho
# rhum: Umidade relativa (%)
# wdir: Direção do vento (°)
# wspd: Velocidade do vento (km/h)
# wpgt: Rajadas (wind gust)
# pres: Pressão atmosférica (hPa)
# coco: Código de cobertura de nuvem
# tsun: Duração de insolação (min)

from meteostat import Stations, Hourly
from datetime import datetime
import pandas as pd

# Procurar a estação SCRM por ICAO
stations = Stations()
stations = stations.fetch()

# Filtrar manualmente pelo código ICAO
station = stations[stations['icao'] == 'SCRM']

if station.empty:
    print("Estação SCRM não encontrada.")
else:
    station_id = station.index[0]
    print(f"Estação encontrada: {station.loc[station_id]['name']}")

    # Definir período
    start = datetime(2010, 1, 1)
    end = datetime(2025, 6, 30)

    # Baixar série horária
    data = Hourly(station_id, start, end)
    df = data.fetch()

    #print(df.head())
    print(f"Número de registros disponíveis: {len(df)}")
    print(f"De: {df.index.min()} até {df.index.max()}")

    #print(df['wpgt'].dropna())
    #print(df[['wspd', 'wpgt']].dropna())

    # Converter velocidade do vento de km/h para nós
    #df['wspd_knots'] = (df['wspd'] / 1.852).round(2)
    #df['wpgt_knots'] = (df['wpgt'] / 1.852).round(2)

# Salvar em arquivo CSV
    df.to_csv('metar_frei_20100101_20250630-novoteste.csv')
    print("Arquivo salvo como metar_frei_20100101_20250630-novoteste.csv")
