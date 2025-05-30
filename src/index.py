# a python script to call a rest endpoint for raspberry priimport requests

#!/bin/bash
import requests
import json
import time
import board
import neopixel
import pathlib
import asyncio

data_pin = board.D18
order = neopixel.RGBW
number_of_pixels = 118
pixel = neopixel.NeoPixel(data_pin, number_of_pixels, brightness=0.5, auto_write=True, pixel_order=order)

appInfo = json.loads(pathlib.Path("./appInfo.json").read_text())

mock_response = json.loads(pathlib.Path("./mockResponse.json").read_text())

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
        # current_weather = None

class Trend:
    def __init__(self):
        self.temp = "No Change"
        self.precipitation = False

async def get_weather_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching data: {e}")
        return None

async def monitor_weather_trend(trend):
    while True:
        global current_weather
        global temperature_tolerance
        print("Fetching weather data...")
        api_url = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely,alerts,current&units=imperial&appid={appId}".format(lat = appInfo["lat"], lon = appInfo["lon"], appId = appInfo["appId"])
        # weather_data = await get_weather_data(api_url)
        weather_data = mock_response # Simulated data for testing
        # if weather_data:
        #     print("Weather Data:")
        #     print(json.dumps(weather_data, indent=4))
        #     raise Exception("just once")

        # if current_weather is None:
        #     current_weather = weather_data["daily"][0]

        # tomorrow = weather_data["daily"][0]

        # temp_today = current_weather["temp"]["day"]
        # temp_tomorrow = tomorrow["temp"]["day"]

        # if temp_tomorrow > (temp_today + appInfo["temperature_tolerance"]):
        #     print("Warmer")
        #     trend.temp = "Warmer"

        # elif temp_tomorrow < (temp_today - appInfo["temperature_tolerance"]):
        #     print("Cooler")
        #     trend.temp = "Colder"
        # else:
        #     print("No Change")
        #     trend.temp = "No Change"

        # if tomorrow["pop"] >= 0.5:
        #     print("Rain is expected tomorrow.")
        #     trend.precipitation = True
        # else:
        #     print("No rain expected tomorrow.")
        #     trend.precipitation = False

        #test cycle
        trend.precipitation = False

        if trend.temp == "Warmer":
            trend.temp = "Colder"
        elif trend.temp == "Colder":
            trend.temp = "No Change"
        else:
            trend.temp = "Warmer"
        # current_weather = tomorrow  # Update current weather for the next iteration
        await asyncio.sleep(10) # seconds TODO: set to appInfo["weather_update_interval"]

async def drive_pixels(trend):
    overall_brightness = 0.0
    while True:
        if trend.temp == "Warmer":
            color = (255, 0, 0, 0)  # Red
        elif trend.temp == "Colder":
            color = (255, 255, 255, 0)  # White
        else:
            color = (0, 255, 0, 0)  # Green
        pixel.fill(color)
        # pixel.show()

        print("Color:", color)
        #     print(json.dumps(weather_data, indent=4))

        await asyncio.sleep(1)
    
async def main():
    trend = Trend()

    weather_task = asyncio.create_task(monitor_weather_trend(trend))
    pixel_task = asyncio.create_task(drive_pixels(trend))

    await asyncio.gather(weather_task, pixel_task)

asyncio.run(main())