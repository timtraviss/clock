import streamlit as st
import datetime
import time
import requests
import streamlit.components.v1 as components


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

def weather_map():
    api_key = "9da1e341daff5763b692c09221e1ec0e"
    # Zoom Level 
    z = 7
    # number of x tile coordinate
    x = 0
    # number of y tile coordinate.
    y = 16
    layer = "precipitation_new"
    url = f"https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        st.write("test")
    else:
        st.write("Failed to retrieve weather data")    

# Display the flip clock and Auckland weather

col1, col2= st.columns(2)

with col1:
    flip_clock()
    

with col2:
    get_auckland_weather()

# with col3:
    # weather_map()



# In this code, we use Streamlit to create a webpage, the `datetime` and `time` modules to display the current time, 
# and the `requests` module to fetch the weather from the OpenWeather API. Replace `"YOUR_OPENWEATHER_API_KEY"` with your actual OpenWeather API key. 
# The `get_auckland_weather` function fetches the weather data for Auckland from the OpenWeather API and displays the weather description and temperature 
# in Celsius.
# Please note that you need to sign up for the OpenWeather API and obtain an API key to use the weather data retrieval functionality.
# The search results did not provide a direct example of displaying the time and weather in separate columns, but the provided Python code should 
# help you achieve this using Streamlit and the OpenWeather API.