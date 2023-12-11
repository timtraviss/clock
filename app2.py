import streamlit as st
import datetime
import requests
import streamlit.components.v1 as components
import openweathermapy.core as owm
import pydeck as pdk
import time

# Function to display the current time as a flip clock
def flip_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.metric(label="Time", value=f"{current_time}", delta="none")


def get_auckland_weather():
    api_key = "9da1e341daff5763b692c09221e1ec0e"
    city = "Auckland"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        # feelslike = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        degrees = data['wind']['deg']
        # rain = data['rain']['rain.1h']

        # Convert direction to compass bearing
        def degrees_to_compass(degrees):
            directions = ['North', 'North-Northeast', 'Northeast', 'East-Northeast', 'East',
                  'East-Southeast', 'Southeast', 'South-Southeast', 'South',
                  'South-Southwest', 'Southwest', 'West-Southwest', 'West',
                  'West-Northwest', 'Northwest', 'North-Northwest', 'North']

            index = round(degrees / 22.5) % 16
            return directions[index]

        # Calculates and displays the wind direction
        degree_value = 45  # Replace this with the actual degree value
        compass_direction = degrees_to_compass(degree_value)
        # print(f"{degree_value} degrees corresponds to {compass_direction}")

        st.metric(label="Temperature", value=f"{temperature}°C", delta="none")
        st.metric(label="Weather in Auckland", value=f"{weather_description}", delta="none")
        # st.metric(label="Feels Like", value=f"{feelslike}°C", delta="none")
        st.metric(label="Humidity", value=f"{humidity}%", delta="none")
        st.metric(label="Wind", value=f"{wind}m/s", delta="none")
        st.metric(label="Wind Direction", value=f"{compass_direction} - {degrees}°", delta="none")
        # st.metric(label="Rain",value=f"{rain}1h/mm",delta="none")

    else:
        st.write("Failed to retrieve weather data")


# OpenWeather and Mapbox configurations
API_CONFIG = {
    "openweathermap": {
        "url": "http://api.openweathermap.org/data/2.5/",
        "api_key": "9da1e341daff5763b692c09221e1ec0e",
        "units": "metric",
    },
    "mapbox": {
        "access_token": "pk.eyJ1IjoiZGV0ZWN0aXZlIiwiYSI6ImNFODJ1VjgifQ.W7Qe05bGseWCOThC3YE4uQ",
        "map_style": "mapbox://styles/mapbox/light-v9",
    },
}

AUCKLAND_COORDS = {
    "lat": -36.8485,
    "lon": 174.7633,
}


def get_weather_data(api_config, coords):
    """
    Retrieves weather data from OpenWeatherMap API.

    Args:
        api_config: Dictionary containing OpenWeatherMap API configuration.
        coords: Dictionary containing latitude and longitude coordinates.

    Returns:
        Dictionary containing weather data and rain data.
    """
    params = {
        **coords,
        "appid": api_config["openweathermap"]["api_key"],


        "units": api_config["openweathermap"]["units"],
    }
    response = requests.get(api_config["openweathermap"]["url"] + "onecall", params=params)
    data = response.json()
    
    if 'daily' in data:
        # Extract rain data
        rain_data = []
        for day in data['daily']:
            rain = day.get('rain', {}).get('1h', 0.0)  # Get precipitation for the last hour
            rain_data.append({
                'lat': coords['lat'],
                'lon': coords['lon'],
                'rain': rain
            })
    
    return data, rain_data


while True:
    weather_data, rain_data = get_weather_data(API_CONFIG, AUCKLAND_COORDS)

    deck = pdk.Deck(
        map_style=API_CONFIG["mapbox"]["map_style"],
        initial_view_state=pdk.ViewState(
            latitude=AUCKLAND_COORDS["lat"],
            longitude=AUCKLAND_COORDS["lon"],
            zoom=11,
            pitch=50,
        ),
    )

    # Create a PyDeck layer for rain data if rain data is available
    if rain_data:
        rain_layer = pdk.Layer(
            "ScatterplotLayer",
            data=rain_data,
            get_position='[lon, lat]',
            get_radius='1000',  # Scale the radius for visibility
            get_fill_color='[0, 0, rain * 255, 150]',  # Use blue color based on rain intensity
            pickable=True,
            auto_highlight=True,
        )
        deck.layers.append(rain_layer)



    # Display the PyDeck deck using st.pydeck_chart
    st.pydeck_chart(deck)
    
    get_auckland_weather()
    flip_clock()
    
    time.sleep(60)  # Refresh every 60 seconds
