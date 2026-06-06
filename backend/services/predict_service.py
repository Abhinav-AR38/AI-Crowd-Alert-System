import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model = joblib.load(BASE_DIR / "model" / "crowd_model.pkl")

day_encoder = joblib.load(BASE_DIR / "model" / "day_encoder.pkl")
weather_encoder = joblib.load(BASE_DIR / "model" / "weather_encoder.pkl")
event_encoder = joblib.load(BASE_DIR / "model" / "event_encoder.pkl")
print(event_encoder.classes_)


def predict_crowd(hour, day, weather, event):

    data = pd.DataFrame({
        "hour": [hour],
        "day": [day_encoder.transform([day])[0]],
        "weather": [weather_encoder.transform([weather])[0]],
        "event": [event_encoder.transform([event])[0]]
    })

    prediction = model.predict(data)[0]

    return round(float(prediction), 2)