# AI Crowd Alert & Safe Route Recommendation System

## Overview

The AI Crowd Alert & Safe Route Recommendation System predicts crowd congestion levels using Machine Learning and generates safer routes using the A* pathfinding algorithm.

The system combines:

* Crowd Risk Prediction (XGBoost)
* Safe Route Planning (A*)
* Real-Time Weather Integration
* Interactive Map Visualization
* Crowd Zone Monitoring
* Auto Refresh Dashboard

---

## Features

### Crowd Risk Prediction

Predicts crowd density based on:

* Hour
* Day
* Weather
* Event Type

### Safe Route Recommendation

Generates routes that avoid high-risk crowd zones.

### Live Crowd Monitoring

Displays risk levels for monitored locations:

* Mugaliwakkam
* Ramapuram
* Manapakkam

### Weather Integration

Fetches real-time weather information and incorporates it into crowd-risk estimation.

### Interactive Map

Built with React Leaflet and OpenStreetMap.

---

## Technology Stack

### Frontend

* React
* Vite
* React Leaflet
* Axios

### Backend

* FastAPI
* Python

### Machine Learning

* XGBoost Regressor
* Scikit-Learn
* Pandas

### Mapping

* OSMnx
* NetworkX
* OpenStreetMap

---

## Project Structure

```text
AI-Crowd-Alert-System
│
├── backend
│   ├── services
│   └── main.py
│
├── dataset
│   ├── generate_dataset.py
│   └── crowd_dataset.csv
│
├── model
│   ├── train_model.py
│   ├── crowd_model.pkl
│   └── encoders
│
└── frontend
    ├── src
    └── public
```

---

## API Endpoints

### Crowd Zones

```http
GET /crowd-zones
```

Returns current crowd risk levels.

### Route Generation

```http
GET /route
```

Returns a safe route between source and destination.

### Weather

```http
GET /weather
```

Returns current weather conditions.

### Prediction

```http
GET /predict
```

Returns crowd risk prediction.

---

## Example Output

```json
{
  "crowd_risk": 97.84
}
```

---

## Future Enhancements

* IoT Sensor Integration
* CCTV-Based Crowd Detection
* Mobile Application
* Multi-City Monitoring
* Emergency Evacuation Planning

---


