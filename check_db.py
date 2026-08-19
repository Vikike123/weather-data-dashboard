import sqlite3

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

print("--- Cities tábla ---")
cursor.execute("SELECT * FROM cities")
for row in cursor.fetchall():
    print(row)

print("\n--- Weather_data tábla ---")
cursor.execute("SELECT * FROM weather_data")
for row in cursor.fetchall():
    print(row)

conn.close()