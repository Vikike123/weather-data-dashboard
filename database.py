import sqlite3

DB_NAME = "weather.db"

def create_tables():
    """Létrehozza a szükséges táblákat, ha még nem léteznek."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            precipitation REAL,
            wind_speed REAL,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
    """)

    conn.commit()
    conn.close()

def insert_city(name, lat, lon):
    """Beszúr egy várost, ha még nincs a táblában. Visszaadja a city_id-t."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM cities WHERE name = ?", (name,))
    row = cursor.fetchone()

    if row:
        city_id = row[0]
    else:
        cursor.execute("INSERT INTO cities (name, lat, lon) VALUES (?, ?, ?)", (name, lat, lon))
        city_id = cursor.lastrowid
        conn.commit()

    conn.close()
    return city_id

def insert_weather(city_id, date, temperature, humidity, precipitation, wind_speed):
    """Beszúr egy időjárási rekordot."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO weather_data (city_id, date, temperature, humidity, precipitation, wind_speed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (city_id, date, temperature, humidity, precipitation, wind_speed))

    conn.commit()
    conn.close()