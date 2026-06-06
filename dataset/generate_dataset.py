import pandas as pd
import random

rows = []

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weather_conditions = [
    "Clear",
    "Cloudy",
    "Rain"
]

events = [
    "NoEvent",
    "Concert",
    "Festival",
    "Sports"
]

for _ in range(10000):

    hour = random.randint(0, 23)

    day = random.choice(days)

    weather = random.choice(weather_conditions)

    event = random.choice(events)

    crowd = 20

    if day in ["Saturday", "Sunday"]:
        crowd += 20

    if event != "None":
        crowd += 40

    if weather == "Rain":
        crowd -= 10

    if 17 <= hour <= 21:
        crowd += 20

    crowd += random.randint(-10, 10)

    crowd = max(0, min(100, crowd))

    rows.append([
        hour,
        day,
        weather,
        event,
        crowd
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "hour",
        "day",
        "weather",
        "event",
        "crowd_risk"
    ]
)

df.to_csv("crowd_dataset.csv", index=False)

print("Dataset generated")