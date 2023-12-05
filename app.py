import streamlit as st
import datetime
import time
import requests
import streamlit.components.v1 as components
import openweathermapy.core as owm
import folium
import json
import pydeck as pdk

# import streamlit as st from streamlit_autorefresh 
# import st_autorefresh 
# Run the autorefresh every second and stop after a certain number of refreshes count 
# = st_autorefresh(interval=1000, limit=100, key="refresh_counter") # Your app logic here 

# st.title('Kia ora')

st.set_page_config(
    page_title="Weather",
    page_icon=":thumb",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Function to display the current time as a flip clock
def flip_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.header(current_time)
    # st.rerun()
    
# Function to fetch the weather from Auckland
# https://openweathermap.org/current
def get_auckland_weather():
    api_key = "9da1e341daff5763b692c09221e1ec0e"
    city = "Auckland"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feelslike = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        st.metric(label="Temperature", value=f"{temperature}°C", delta="none")
        st.metric(label="Weather in Auckland", value=f"{weather_description}", delta="none")
        st.metric(label="Feels Like", value=f"{feelslike}°C", delta="none")
        st.metric(label="Humidity", value=f"{humidity}%", delta="none")
        st.metric(label="Wind", value=f"{wind}m/s", delta="none")

    else:
        st.write("Failed to retrieve weather data")
  

# Function to fetch weather data from the OpenWeatherMap API
# api_key = "9da1e341daff5763b692c09221e1ec0e"
# city = "Auckland"

# def fetch_weather_data(city, api_key):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
#     response = requests.get(url)
#     data = json.loads(response.text)
#     return data


# OpenWeather API key (replace 'YOUR_API_KEY' with your actual API key)

API_KEY = '9da1e341daff5763b692c09221e1ec0e'
AUCKLAND_COORDS = {'lat': -36.8485, 'lon': 174.7633}
API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Mapbox access token (replace with your own token)
MAPBOX_TOKEN = "pk.eyJ1IjoiZGV0ZWN0aXZlIiwiYSI6ImNFODJ1VjgifQ.W7Qe05bGseWCOThC3YE4uQ"

# Auckland coordinates
AUCKLAND_COORDS = {'lat': -36.8485, 'lon': 174.7633}

# OpenWeatherMap API key (replace with your actual key)
OPENWEATHERMAP_API_KEY = "9da1e341daff5763b692c09221e1ec0e"

# Auckland coordinates
AUCKLAND_COORDS = {'lat': -36.8485, 'lon': 174.7633}

# Function to get weather data from OpenWeatherMap API
def get_weather_data(api_key, coords):
    api_url = 'http://api.openweathermap.org/data/2.5/onecall'
    params = {
        'lat': coords['lat'],
        'lon': coords['lon'],
        'appid': api_key,
        'exclude': 'current,minutely,hourly',  # Exclude unnecessary data
        'units': 'metric'
    }
    response = requests.get(api_url, params=params)
    return response.json()

# Get weather data for Auckland
weather_data = get_weather_data(OPENWEATHERMAP_API_KEY, AUCKLAND_COORDS)

# Create a PyDeck deck
deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=AUCKLAND_COORDS['lat'],
        longitude=AUCKLAND_COORDS['lon'],
        zoom=9,
        pitch=50,
    ),
)

#Display two columns
col1, col2 = st.columns([3,1], gap="medium")

with col1:
    # st.map(data=None, latitude=-36.8485, longitude=174.7633, zoom=16)
    # Check if weather data is available
    if 'daily' in weather_data:
    # Extract rain data
        rain_data = [{'lat': AUCKLAND_COORDS['lat'],
                  'lon': AUCKLAND_COORDS['lon'],
                  'rain': day['rain'] if 'rain' in day else 0.0}
                 for day in weather_data['daily']]

    # Create a PyDeck layer for rain data
    rain_layer = pdk.Layer(
        "ScatterplotLayer",
        data=rain_data,
        get_position='[lon, lat]',
        get_radius='rain * 1000',  # Scale the radius for visibility
        get_fill_color='[0, 0, rain * 255, 150]',  # Use blue color based on rain intensity
        pickable=True,
        auto_highlight=True,
    )

    # Create a PyDeck deck
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[rain_layer],
        initial_view_state=pdk.ViewState(
            latitude=AUCKLAND_COORDS['lat'],
            longitude=AUCKLAND_COORDS['lon'],
            zoom=10,
            pitch=50,
        ),
    )

    # Display the PyDeck deck using st.pydeck_chart
    st.pydeck_chart(deck)
        # else:
        #     st.error("Error fetching weather data from OpenWeatherMap.")
    

with col2:
    get_auckland_weather()

