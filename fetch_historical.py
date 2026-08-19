import requests
from database import create_tables, insert_city, insert_weather

CITIES = [
    {"name": "Szeged", "lat": 46.2530, "lon": 20.1414},
    {"name": "Budapest", "lat": 47.4979, "lon": 19.0402},
    {"name": "Vésztő", "lat": 46.9167, "lon": 21.2667},
]

def get_historical_weather(lat, lon, start_date, end_date):
    """Lekéri a napi időjárási adatokat egy adott időszakra."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max",
        "timezone": "Europe/Budapest"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    create_tables()

    # Utolsó 30 nap adatai
    start_date = "2026-07-01"
    end_date = "2026-07-31"

    for city in CITIES:
        data = get_historical_weather(city["lat"], city["lon"], start_date, end_date)
        city_id = insert_city(city["name"], city["lat"], city["lon"])

        daily = data["daily"]
        dates = daily["time"]

        for i in range(len(dates)):
            insert_weather(
                city_id=city_id,
                date=dates[i],
                temperature=daily["temperature_2m_mean"][i],
                humidity=daily["relative_humidity_2m_mean"][i],
                precipitation=daily["precipitation_sum"][i],
                wind_speed=daily["wind_speed_10m_max"][i]
            )

        print(f"{city['name']}: {len(dates)} napi rekord elmentve.")

if __name__ == "__main__":
    main()