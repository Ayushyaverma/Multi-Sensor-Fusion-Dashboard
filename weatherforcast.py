import requests
import pandas as pd

def get_live_weather(api_key, lat, lon):
    """
    Fetches live weather data from OpenWeatherMap.
    Returns a dictionary with temperature, humidity, description, and wind speed.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "desc": data["weather"][0]["description"].capitalize(),
                "wind": data["wind"]["speed"]
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def get_mock_forecast():
    """
    Returns mock forecast data for visualization when API is not available
    or for demonstration purposes.
    """
    return pd.DataFrame({
        "Time": ["12:00", "15:00", "18:00", "21:00", "00:00"],
        "Temperature": [25, 24, 22, 20, 18],
        "Humidity": [60, 55, 50, 45, 40]
    })