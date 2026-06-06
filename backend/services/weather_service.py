import requests

API_KEY = "5d11cd135def3256628714a684974dc7"

def get_weather():

    lat = 13.0215
    lon = 80.1670

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    weather = data["weather"][0]["main"]

    print("Current Weather:", weather)

    if weather in ["Rain", "Drizzle", "Thunderstorm"]:
        return "Rain"

    elif weather in ["Clouds", "Mist", "Fog", "Haze"]:
        return "Cloudy"

    else:
        return "Clear"