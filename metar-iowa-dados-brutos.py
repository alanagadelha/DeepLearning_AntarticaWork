import requests

url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
params = {
    "station": "SCRM",
    "data": "metar",
    "year1": 2017,
    "month1": 1,
    "day1": 1,
    "year2": 2025,
    "month2": 6,
    "day2": 20,
    "tz": "Etc/UTC",
    "format": "onlycomma",
    "direct": "yes"
}

r = requests.get(url, params=params)

with open("scrm_metar.csv", "w") as f:
    f.write(r.text)
