import tkinter as tk
from tkinter import messagebox
import requests

# APIs
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

HEADERS = {
    "User-Agent": "WeatherApp"
}

# Weather codes
weather_codes = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Cloudy", "☁️"),
    45: ("Fog", "🌫"),
    61: ("Rain", "🌧"),
    71: ("Snow", "❄️"),
    95: ("Thunderstorm", "⛈")
}


# Get city coordinates
def geocode(city):

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    response = requests.get(
        GEOCODE_URL,
        params=params,
        headers=HEADERS
    )

    data = response.json()

    if not data:
        return None

    lat = data[0]["lat"]
    lon = data[0]["lon"]
    name = data[0]["display_name"]

    return lat, lon, name


# Get weather
def fetch_weather(lat, lon):

    params = {
        "latitude": lat,
        "longitude": lon,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "wind_speed_10m",
            "weather_code"
        ],

        "timezone": "auto"
    }

    response = requests.get(
        WEATHER_URL,
        params=params
    )

    return response.json()


# Show weather
def get_weather():

    city = city_entry.get()

    if city == "":
        messagebox.showerror(
            "Error",
            "Please enter city name"
        )
        return

    try:

        location = geocode(city)

        if location is None:
            messagebox.showerror(
                "Error",
                "City not found"
            )
            return

        lat, lon, city_name = location

        weather_data = fetch_weather(lat, lon)

        current = weather_data["current"]

        code = current["weather_code"]

        label, emoji = weather_codes.get(
            code,
            ("Unknown", "🌡")
        )

        result = f"""
{emoji} Weather: {label}

🌡 Temperature: {current['temperature_2m']}°C

🤔 Feels Like: {current['apparent_temperature']}°C

💧 Humidity: {current['relative_humidity_2m']}%

💨 Wind Speed: {current['wind_speed_10m']} km/h
"""

        messagebox.showinfo(
            "Weather App",
            result
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# Main window
root = tk.Tk()

root.title("Weather App")

root.geometry("400x250")


# Title
title_label = tk.Label(
    root,
    text="Enter City Name",
    font=("Arial", 20)
)

title_label.pack(pady=10)


# Input
city_entry = tk.Entry(
    root,
    font=("Arial", 16),
    width=25
)

city_entry.pack(pady=10)


# Button
search_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 14),
    command=get_weather
)

search_button.pack(pady=10)


# Run app
root.mainloop()