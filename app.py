import streamlit as st
import datetime
import requests
import streamlit.components.v1 as components
import openweathermapy.core as owm
import pydeck as pdk
import time

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
# def flip_clock():
#     current_time = datetime.datetime.now().strftime("%H:%M:%S")
#     # st.subheader(current_time)
#     st.metric(label="Time", value=f"{current_time}", delta="none")
#     # st.rerun()

def flip_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.metric(label="Time", value=f"{current_time}", delta="none")


    
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
        # feelslike = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        degrees = data['wind']['deg']
        # rain = data['rain']['rain.1h']

        # Convert direction to compass bearing
        def degrees_to_compass(degrees):
            directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

            index = round(degrees / 22.5) % 8
            return directions[index]

        # Calculates and displays the wind direction 
        degree_value = 45  # Replace this with the actual degree value
        compass_direction = degrees_to_compass(degree_value)
        print(f"{degree_value} degrees corresponds to {compass_direction}")

        st.metric(label="Temperature", value=f"{temperature}°C", delta="none")
        st.metric(label="Weather in Auckland", value=f"{weather_description}", delta="none")
        # st.metric(label="Feels Like", value=f"{feelslike}°C", delta="none")
        st.metric(label="Humidity", value=f"{humidity}%", delta="none")
        st.metric(label="Wind", value=f"{wind}m/s", delta="none")
        st.metric(label="Wind Direction", value=f"{compass_direction} | {degrees}°", delta="none")
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
        Dictionary containing weather data.
    """
    params = {
        **coords,
        "appid": api_config["openweathermap"]["api_key"],
        "units": api_config["openweathermap"]["units"],
    }
    response = requests.get(api_config["openweathermap"]["url"] + "onecall", params=params)
    return response.json()

weather_data = get_weather_data(API_CONFIG, AUCKLAND_COORDS)

deck = pdk.Deck(
    map_style=API_CONFIG["mapbox"]["map_style"],
    initial_view_state=pdk.ViewState(
        latitude=AUCKLAND_COORDS["lat"],
        longitude=AUCKLAND_COORDS["lon"],
        zoom=9,
        pitch=50,
    ),
)


#Display two columns
col1, col2, col3 = st.columns([2,1,1], gap="medium")

with col1:
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
            zoom=11,
            pitch=50,
        ),
    )

    # Display the PyDeck deck using st.pydeck_chart
    st.pydeck_chart(deck)
        
with col2:
    get_auckland_weather()
    
with col3:
   flip_clock()
   time.sleep(60)
   if st.button("Reload Page"):
    st.rerun()



