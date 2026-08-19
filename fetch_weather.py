import requests
from datetime import datetime
from database import create_tables, insert_city, insert_weather

CITIES = [
    {"name": "Szeged", "lat": 46.2530, "lon": 20.1414},
    {"name": "Budapest", "lat": 47.4979, "lon": 19.0402},
    {"name": "Vésztő", "lat": 46.9167, "lon": 21.2667},
]

def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "Europe/Budapest"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    create_tables()  # biztosítjuk, hogy a táblák léteznek

    for city in CITIES:
        data = get_weather(city["lat"], city["lon"])
        current = data["current"]

        city_id = insert_city(city["name"], city["lat"], city["lon"])

        insert_weather(
            city_id=city_id,
            date=current["time"],
            temperature=current["temperature_2m"],
            humidity=current["relative_humidity_2m"],
            precipitation=current["precipitation"],
            wind_speed=current["wind_speed_10m"]
        )

        print(f"{city['name']} adatai elmentve: {current['temperature_2m']}°C")

if __name__ == "__main__":
    main()