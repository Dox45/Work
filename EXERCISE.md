# Debugging exercise: weather report

A small Python script that reports the current weather for one or more cities.
It uses Open-Meteo, a free weather API. No key and no account needed.

## What it should do

Run it with one or more city names:

```
python3 weather_report.py Lagos
python3 weather_report.py Lagos Abuja London
```

For every city given, in the order the cities were given, it should print one
line in this shape:

```
Lagos: 30.0 C (86.0 F), wind 15.3 km/h - mild
```

The rules for that line:

- The city name as the geocoding service returns it, then the current
  temperature in Celsius to one decimal place.
- The same temperature in Fahrenheit in brackets, using the proper conversion:
  Celsius x 9 / 5 + 32.
- The current wind speed in km/h, one decimal place.
- A comfort tag: `hot` when the temperature is above 30 C, `cold` when it is
  below 15 C, otherwise `mild`.
- `, windy` at the end when the wind is above 20 km/h.

With no arguments at all, it should report on Lagos.

If a city cannot be found, it should say so for that city and carry on with the
rest, without crashing.

## Setup

```
pip install -r requirements.txt
```

No API key, no environment variables, nothing to sign up for.

## The task

The script is meant to run end to end and match the rules above. It does not.
Today it stops with an error before printing anything useful, and at least one
part of the logic is wrong even where it does run.

Find the defects, fix them, and make the output match the rules. Some of them
are simple typos. At least one is a design mistake that hides the others, so
fixing that one first makes the rest easier to see. At least one produces no
error at all, just a wrong number.
