# a python script to call a rest endpoint for raspberry priimport requests

#!/bin/bash
import requests
import json
import time
# import board
# import neopixel
import pathlib

# DATA_PIN = board.D10
# pixel = neopixel.NeoPixel(DATA_PIN, 30)

appInfo = json.loads(pathlib.Path("./appInfo.json").read_text())

# current_weather = None
current_weather = {
            "dt": 1737223200,
            "sunrise": 1737207910,
            "sunset": 1737241134,
            "moonrise": 1737260340,
            "moonset": 1737216480,
            "moon_phase": 0.66,
            "summary": "Expect a day of partly cloudy with clear spells",
            "temp": {
                "day": 253.54,
                "min": 252.62,
                "max": 261.88,
                "night": 252.62,
                "eve": 257.29,
                "morn": 259.09
            },

            "feels_like": {
                "day": 252.54,
                "night": 245.62,
                "eve": 250.29,
                "morn": 252.09
            },
            "pressure": 1026,
            "humidity": 51,
            "dew_point": 252.37,
            "wind_speed": 8.08,
            "wind_deg": 332,
            "wind_gust": 14.58,
            "weather": [
                {
                    "id": 801,
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d"
                }
            ],
            "clouds": 11,
            "pop": 0,
            "uvi": 0.97
        }
tempature_tolerance = 5

def get_weather_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    print("Fetching weather data...")
    api_url = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely&appid={appId}".format(lat = appInfo["lat"], lon = appInfo["lon"], appId = appInfo["appId"])
    weather_data = get_weather_data(api_url)
    if weather_data:
        print("Weather Data:")
        print(json.dumps(weather_data, indent=4))

    global current_weather
    if current_weather is None:
        current_weather = weather_data["daily"][0]

    tomorrow = weather_data["daily"][0]

    temp_today = current_weather["temp"]["day"]
    temp_tomorrow = tomorrow["temp"]["day"]

    if temp_tomorrow > temp_today + tempature_tolerance:
        print("Red")

    elif temp_tomorrow < temp_today - tempature_tolerance:
        print("White")

    else:
        print("Green")

    if tomorrow["pop"] >= 0.5:
        print("Rain is expected tomorrow.")
    else:
        print("No rain expected tomorrow.")

# while True:
main()
    # time.sleep(60)