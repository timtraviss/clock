import streamlit as st
import datetime
import time
import requests

st.title('Time and Weather')

# Function to display the current time as a flip clock
def flip_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.write(current_time)

# Function to fetch the weather from Auckland
def get_auckland_weather():
    api_key = "YOUR_OPENWEATHER_API_KEY"
    city = "Auckland"
    url = fhttp://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        st.write(f"Weather in Auckland: {weather_description}, Temperature: {temperature}°C")
    else:
        st.write("Failed to retrieve weather data")

# Display the flip clock and Auckland weather
flip_clock()
get_auckland_weather()


# In this code, we use Streamlit to create a webpage, the `datetime` and `time` modules to display the current time, 
# and the `requests` module to fetch the weather from the OpenWeather API. Replace `"YOUR_OPENWEATHER_API_KEY"` with your actual OpenWeather API key. 
# The `get_auckland_weather` function fetches the weather data for Auckland from the OpenWeather API and displays the weather description and temperature 
# in Celsius.
# Please note that you need to sign up for the OpenWeather API and obtain an API key to use the weather data retrieval functionality.
# The search results did not provide a direct example of displaying the time and weather in separate columns, but the provided Python code should 
# help you achieve this using Streamlit and the OpenWeather API.