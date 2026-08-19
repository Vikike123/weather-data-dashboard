import numpy as np

# Tömb létrehozása
np.array([1, 2, 3])
np.zeros(5)              # csupa 0 tömb
np.ones(5)                # csupa 1 tömb
np.arange(0, 10, 2)       # 0-tól 10-ig, 2-es lépésközzel
np.linspace(0, 1, 5)      # 5 egyenletesen elosztott érték 0 és 1 között

# Statisztikai műveletek (pl. hőmérséklet adatokon)
np.mean(arr)               # átlag
np.median(arr)             # medián
np.std(arr)                 # szórás
np.min(arr) / np.max(arr)   # minimum / maximum
np.sum(arr)                 # összeg

# Szűrés, keresés
arr[arr > 30]                       # csak a 30 fölötti értékek
np.where(arr > 30)                  # a feltételnek megfelelő indexek
np.isnan(arr)                        # hiányzó (NaN) értékek keresése

# Tömb alakja / átalakítása
arr.shape
arr.reshape(3, 4)
np.concatenate([arr1, arr2])


import pandas as pd

# Beolvasás / mentés
pd.read_csv("file.csv")
pd.read_sql_query("SELECT * FROM table", conn)   # a dashboard.py-ban is használva
df.to_csv("output.csv", index=False)

# Alap felfedezés
df.head()          # első 5 sor
df.info()           # oszlopok, típusok, hiányzó értékek
df.describe()        # statisztikai összefoglaló
df.shape              # (sorok, oszlopok)
df.columns             # oszlopnevek

# Szűrés, kiválasztás
df["temperature"]                          # egy oszlop
df[df["temperature"] > 30]                  # feltételes szűrés
df.loc[df["city"] == "Szeged"]              # cím szerinti szűrés
df.iloc[0:5]                                  # pozíció szerinti szűrés

# Hiányzó / duplikált adatok kezelése (Data Quality)
df.isnull().sum()          # hiányzó értékek oszloponként
df.dropna()                  # hiányzó sorok eldobása
df.fillna(0)                  # hiányzó értékek pótlása
df.duplicated()                # duplikátumok keresése
df.drop_duplicates()             # duplikátumok törlése

# Csoportosítás, összesítés
df.groupby("city")["temperature"].mean()
df.sort_values("date")
df.pivot_table(index="date", columns="city", values="temperature")   # a dashboard.py-ban is használva

# Összekapcsolás (join / adatintegráció)
pd.merge(df1, df2, on="city_id")


import sqlite3

# Kapcsolódás
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# Tábla létrehozása
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
""")

# Adat beszúrása
cursor.execute("INSERT INTO cities (name) VALUES (?)", ("Szeged",))
conn.commit()          # mentés nélkül nem íródik ki a változás

# Lekérdezés
cursor.execute("SELECT * FROM cities")
cursor.fetchall()        # összes sor
cursor.fetchone()          # csak egy sor

# Frissítés / törlés
cursor.execute("UPDATE cities SET name = ? WHERE id = ?", ("Budapest", 1))
cursor.execute("DELETE FROM cities WHERE id = ?", (1,))

# Szűrés, rendezés, csoportosítás (tiszta SQL, execute-on belül)
cursor.execute("SELECT * FROM weather_data WHERE temperature > 30")
cursor.execute("SELECT * FROM weather_data ORDER BY date DESC")
cursor.execute("SELECT city_id, AVG(temperature) FROM weather_data GROUP BY city_id")

# Lezárás
conn.close()              # mindig zárd le a kapcsolatot a végén