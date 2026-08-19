import sqlite3
import pandas as pd
import streamlit as st

DB_NAME = "weather.db"

def load_data():
    """Betölti az összes időjárási adatot, várossal összekapcsolva."""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT c.name AS city, w.date, w.temperature, w.humidity, w.precipitation, w.wind_speed
        FROM weather_data w
        JOIN cities c ON w.city_id = c.id
        ORDER BY w.date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(page_title="Időjárás Dashboard", layout="wide")
    st.title("🌤️ Időjárás-elemző Dashboard")
    st.write("Magyar városok aktuális időjárási adatai, Open-Meteo API-ból gyűjtve.")

    df = load_data()

    if df.empty:
        st.warning("Nincs még adat az adatbázisban. Futtasd le a fetch_weather.py-t!")
        return

    # Legfrissebb adatok városonként
    st.subheader("Legfrissebb mérések")
    latest = df.sort_values("date").groupby("city").last().reset_index()
    display_table = latest[["city", "date", "temperature", "humidity", "precipitation", "wind_speed"]].rename(
        columns={
            "city": "Város",
            "date": "Dátum",
            "temperature": "Hőmérséklet (°C)",
            "humidity": "Páratartalom (%)",
            "precipitation": "Csapadék (mm)",
            "wind_speed": "Szélsebesség (km/h)"
        }
    )
    st.dataframe(display_table)

    # Városok összehasonlítása oszlopdiagramon
    st.subheader("Városok összehasonlítása (legfrissebb adat)")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Hőmérséklet (°C)")
        st.bar_chart(latest.set_index("city")["temperature"])

    with col2:
        st.write("Szélsebesség (km/h)")
        st.bar_chart(latest.set_index("city")["wind_speed"])

    # Hőmérséklet-trend grafikon
    st.subheader("Hőmérséklet alakulása időben (2026.július) ")
    # Hőmérséklet-trend grafikon itt csak a júliust szeretném megmutatni
    df_july = df[df["date"].str.startswith("2026-07")]
    temp_pivot = df_july.pivot_table(index="date", columns="city", values="temperature", aggfunc="mean")
    st.line_chart(temp_pivot)

    # Csapadék-trend grafikon
    st.subheader("Páratartalom alakulása időben (2026. július)")
    df_july = df[df["date"].str.startswith("2026-07")]
    precip_pivot = df_july.pivot_table(index="date", columns="city", values="humidity", aggfunc="mean")
    st.line_chart(precip_pivot)

    # Csapadék-trend grafikon
    st.subheader("Csapadékmennyiség alakulása időben (2026. július)")
    df_july = df[df["date"].str.startswith("2026-07")]
    precip_pivot = df_july.pivot_table(index="date", columns="city", values="precipitation", aggfunc="mean")
    st.line_chart(precip_pivot)

    # Csapadék-trend grafikon
    st.subheader("Szélsebesség alakulása időben (2026. július)")
    df_july = df[df["date"].str.startswith("2026-07")]
    precip_pivot = df_july.pivot_table(index="date", columns="city", values="wind_speed", aggfunc="mean")
    st.line_chart(precip_pivot)


if __name__ == "__main__":
    main()