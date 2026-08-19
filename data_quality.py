import sqlite3

DB_NAME = "weather.db"

def remove_duplicates():
    """Eltávolítja a pontosan egyező duplikátum rekordokat, csak az elsőt megtartva."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM weather_data
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM weather_data
            GROUP BY city_id, date, temperature, humidity, precipitation, wind_speed
        )
    """)

    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    print(f"{deleted} duplikátum rekord törölve.")

def check_missing_values():
    """Ellenőrzi, van-e NULL érték a fontos oszlopokban."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, city_id, date FROM weather_data
        WHERE temperature IS NULL OR humidity IS NULL
           OR precipitation IS NULL OR wind_speed IS NULL
    """)
    missing = cursor.fetchall()

    if missing:
        print(f"FIGYELEM: {len(missing)} rekordban hiányzó érték található:")
        for row in missing:
            print(row)
    else:
        print("Nincs hiányzó érték.")

    conn.close()

def check_outliers():
    """Ellenőrzi, van-e irreálisan extrém hőmérséklet érték."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, city_id, date, temperature FROM weather_data
        WHERE temperature < -40 OR temperature > 50
    """)
    outliers = cursor.fetchall()

    if outliers:
        print(f"FIGYELEM: {len(outliers)} irreális hőmérséklet-érték található:")
        for row in outliers:
            print(row)
    else:
        print("Nincs irreális kiugró érték.")

    conn.close()

if __name__ == "__main__":
    remove_duplicates()
    check_missing_values()
    check_outliers()