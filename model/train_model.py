import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

# Load dataset
df = pd.read_csv("../dataset/crowd_dataset.csv")

# Encode categorical columns
day_encoder = LabelEncoder()
weather_encoder = LabelEncoder()
event_encoder = LabelEncoder()

df["day"] = day_encoder.fit_transform(df["day"])
df["weather"] = weather_encoder.fit_transform(df["weather"])
df["event"] = event_encoder.fit_transform(df["event"])

# Features and target
X = df[["hour", "day", "weather", "event"]]
y = df["crowd_risk"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1
)

model.fit(X_train, y_train)

# Accuracy
score = model.score(X_test, y_test)

print(f"Model R² Score: {score:.4f}")

# Save model and encoders
joblib.dump(model, "crowd_model.pkl")
joblib.dump(day_encoder, "day_encoder.pkl")
joblib.dump(weather_encoder, "weather_encoder.pkl")
joblib.dump(event_encoder, "event_encoder.pkl")

print("Model saved successfully!")