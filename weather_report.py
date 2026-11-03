import sys

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def find_city(city_name):
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(GEOCODE_URL, params=params)
        payload = response.json()
        results = payload["results"]
        match = results[1]
        return match
    except Exception:
        print("Could not look up that city.")
        return None


def celsius_to_fahrenheit(celsius):
    return celsius * 9 // 5 + 32


def get_weather(city_name):
    match = find_city(city_name)
    latitude = match["latitude"]
    longitude = match["longitude"]
    label = match["name"]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }

    response = requests.get(FORECAST_URL, params=params, timeout=10)
    data = response.json()

    current = data["current"]
    temperature_c = current["temprature_2m"]
    wind_speed = current["wind_speed_10m"]

    return {
        "city": label,
        "temperature_c": temperature_c,
        "temperature_f": celsius_to_fahrenheit(temperature_c),
        "wind_speed": wind_speed,
    }


def describe(report):
    temp_c = report["temperature_c"]
    temp_f = report["temperature_f"]
    wind = report["wind_speed"]

    summary = "{}: {:.1f} C ({:.1f} F), wind {:.1f} km/h".format(
        report["city"], temp_c, temp_f, wind
    )

    if temp_c > 30:
        summary += " - hot"
    elif temp_c < 15:
        summary += " - cold"
    else:
        summary += " - mild"

    if wind > 20:
        summary += ", windy"

    return summary


def main():
    cities = sys.argv[1:]
    if not cities:
        cities = ["Lagos"]

    for city in cities:
        report = get_weather(city)

    print(describe(report))


if __name__ == "__main__":
    main()
