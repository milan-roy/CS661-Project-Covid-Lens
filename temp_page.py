import streamlit as st
import pandas as pd
import folium
import requests
import random
from datetime import datetime, timedelta
from folium.plugins import TimestampedGeoJson
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("🗺️ Animated Choropleth Map (30 Days × 3 Countries)")

# --- Dummy Data for 30 Days ---
countries = ['IND', 'AFG', 'FRA']
start_date = datetime(2020, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(30)]

# data = []
# for date in dates:
#     for country in countries:
#         data.append({
#             'date': date.strftime('%Y-%m-%d'),
#             'iso3': country,
#             'value': random.randint(100, 1000)
#         })
# df = pd.DataFrame(data)


@st.cache_data
def generate_dummy_data():
    countries = ['IND', 'AFG', 'FRA']
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(30)]

    data = []
    for date in dates:
        for country in countries:
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'iso3': country,
                'value': random.randint(100, 1000)
            })
    return pd.DataFrame(data)

df = generate_dummy_data()

# --- Load Country Polygons (GeoJSON) ---
geojson_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
world_geojson = requests.get(geojson_url).json()

# --- Build Timestamped GeoJSON Features ---
features = []

for _, row in df.iterrows():
    iso = row['iso3']
    date = row['date']
    value = row['value']

    # Find geometry for this country
    for feature in world_geojson['features']:
        if feature['properties']['iso'] == iso:
            fill_color = f"#{hex(255 - value % 255)[2:].zfill(2)}{hex(value % 255)[2:].zfill(2)}50"
            features.append({
                "type": "Feature",
                "geometry": feature["geometry"],
                "properties": {
                    "time": date,
                    "style": {
                        "color": "black",
                        "weight": 1,
                        "fillColor": fill_color,
                        "fillOpacity": 0.7
                    },
                    "popup": f"{iso} - {value}"
                }
            })
            break

# --- Create Timestamped GeoJSON Layer ---
timestamped_geojson = {
    "type": "FeatureCollection",
    "features": features
}

# --- Initialize Folium Map ---
m = folium.Map(location=[20, 0], zoom_start=2)

TimestampedGeoJson(
    data=timestamped_geojson,
    transition_time=300,
    loop=True,
    auto_play=True,
    add_last_point=True,
    period='P1D'
).add_to(m)

# --- Display Map in Streamlit ---
st.markdown("### 🌍 Time-Animated Country Shapes with Color Based on Dummy Metric")
st_data = st_folium(m, width=1200, height=600)
