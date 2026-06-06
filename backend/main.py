from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.route_service import find_route
from services.predict_service import predict_crowd
from datetime import datetime
from services.predict_service import predict_crowd
from services.weather_service import get_weather

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Crowd Alert API Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/route")
def route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):
    path = find_route(
        start_lat,
        start_lon,
        end_lat,
        end_lon
    )

    return {"route": path}

@app.get("/crowd-zones")
def crowd_zones():

    return {
        "zones": [
            {
                "lat": 13.0225,
                "lon": 80.1685,
                "risk": 90,
                "name": "High Crowd Zone"
            },
            {
                "lat": 13.0260,
                "lon": 80.1710,
                "risk": 70,
                "name": "Medium Crowd Zone"
            },
            {
                "lat": 13.0185,
                "lon": 80.1650,
                "risk": 40,
                "name": "Low Crowd Zone"
            }
        ]
    }
@app.get("/predict")
def predict(
    hour: int,
    day: str,
    weather: str,
    event: str
):
    risk = predict_crowd(
        hour,
        day,
        weather,
        event
    )

    return {
        "crowd_risk": risk
    }
@app.get("/live-crowd")
def live_crowd():

    weather = get_weather()

    zones = [
        {
            "name": "Mugaliwakkam",
            "lat": 13.020,
            "lon": 80.165,
            "risk": predict_crowd(
                18,
                "Saturday",
                weather,
                "Concert"
            )
        },
        {
            "name": "Ramapuram",
            "lat": 13.030,
            "lon": 80.170,
            "risk": predict_crowd(
                14,
                "Saturday",
                weather,
                "Festival"
            )
        },
        {
            "name": "Manapakkam",
            "lat": 13.015,
            "lon": 80.175,
            "risk": predict_crowd(
                9,
                "Monday",
                weather,
                "NoEvent"
            )
        }
    ]

    return {"zones": zones}
@app.get("/weather")
def weather():

    return {
        "weather": get_weather()
    }
