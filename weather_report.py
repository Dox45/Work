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
        response = requests.get(GEOCODE_URL, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except Exception:
        print("Could not look up that city.")
        return None

    results = payload.get("results") or []
    if not results:
        print("Could not find a place called {}.".format(city_name))
        return None

    return results[0]


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def get_weather(city_name):
    match = find_city(city_name)
    if match is None:
        return None

    latitude = match["latitude"]
    longitude = match["longitude"]
    label = match["name"]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current"]
        temperature_c = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]
    except Exception:
        print("Could not fetch the weather for {}.".format(city_name))
        return None

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
        if report is None:
            continue
        print(describe(report))


if __name__ == "__main__":
    main()
