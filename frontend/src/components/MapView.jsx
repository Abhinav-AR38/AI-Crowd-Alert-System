import { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  Circle,
  useMapEvents,
} from "react-leaflet";

import API from "../api/api";

function ClickHandler({
  source,
  destination,
  setSource,
  setDestination,
}) {
  useMapEvents({
    click(e) {
      const point = [e.latlng.lat, e.latlng.lng];

      if (!source) {
        setSource(point);
      } else if (!destination) {
        setDestination(point);
      }
    },
  });

  return null;
}

function MapView() {
  const [source, setSource] = useState(null);
  const [destination, setDestination] = useState(null);
  const [route, setRoute] = useState([]);
  const [crowdZones, setCrowdZones] = useState([]);

  const center = [13.0215, 80.1670];

  // ROUTE FETCH
  useEffect(() => {
    const fetchRoute = async () => {
      if (!source || !destination) return;

      try {
        const response = await API.get("/route", {
          params: {
            start_lat: source[0],
            start_lon: source[1],
            end_lat: destination[0],
            end_lon: destination[1],
          },
        });

        setRoute(response.data.route);
      } catch (error) {
        console.error("Route Error:", error);
      }
    };

    fetchRoute();
  }, [source, destination]);

  // CROWD ZONES + AUTO REFRESH
  useEffect(() => {
    const fetchCrowdZones = async () => {
      try {
        const response = await API.get("/live-crowd");

        setCrowdZones(response.data.zones);
      } catch (error) {
        console.error("Crowd Zone Error:", error);
      }
    };

    fetchCrowdZones();

    const interval = setInterval(fetchCrowdZones, 30000);

    return () => clearInterval(interval);

  }, []);

  // DISTANCE
  const calculateDistance = () => {

  if (route.length < 2) return 0;

  let distance = 0;

  for (let i = 1; i < route.length; i++) {

    const [lat1, lon1] = route[i - 1];
    const [lat2, lon2] = route[i];

    const R = 6371;

    const dLat =
      (lat2 - lat1) * Math.PI / 180;

    const dLon =
      (lon2 - lon1) * Math.PI / 180;

    const a =
      Math.sin(dLat / 2) *
      Math.sin(dLat / 2) +
      Math.cos(lat1 * Math.PI / 180) *
      Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);

    const c =
      2 * Math.atan2(
        Math.sqrt(a),
        Math.sqrt(1 - a)
      );

    distance += R * c;
  }

  return distance.toFixed(2);
};

  // ETA
  const estimateTime = () => {

  const distance =
    Number(calculateDistance());

  const averageSpeed = 20;

  return Math.max(
    1,
    Math.round(
      (distance / averageSpeed) * 60
    )
  );
};
  
  const calculateRouteRisk = () => {

  if (
    route.length === 0 ||
    crowdZones.length === 0
  )
    return 0;

  let totalRisk = 0;
  let affectedPoints = 0;

  route.forEach((point) => {

    crowdZones.forEach((zone) => {

      const latDiff =
        point[0] - zone.lat;

      const lonDiff =
        point[1] - zone.lon;

      const distance =
        Math.sqrt(
          latDiff * latDiff +
          lonDiff * lonDiff
        );

      const zoneRadius =
        (zone.risk * 8) / 111000;

      if (distance <= zoneRadius) {

        totalRisk += zone.risk;
        affectedPoints++;

      }

    });

  });

  if (affectedPoints === 0)
    return 0;

  return totalRisk / affectedPoints;
};

  // SAFETY SCORE
  const safetyScore = () => {

  const routeRisk =
    calculateRouteRisk();

  return Math.max(
    0,
    Math.round(100 - routeRisk)
  );
};

  // RESET
  const resetMap = () => {
    setSource(null);
    setDestination(null);
    setRoute([]);
  };

  return (
    <div
      style={{
        position: "relative",
        height: "100vh",
        width: "100%",
      }}
    >
      {/* RESET BUTTON */}
      <button
        onClick={resetMap}
        style={{
          position: "absolute",
          top: "10px",
          left: "10px",
          zIndex: 1000,
          padding: "10px 15px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Reset
      </button>

      {/* DASHBOARD */}
      <div
        style={{
          position: "absolute",
          top: "10px",
          right: "10px",
          zIndex: 1000,
          backgroundColor: "white",
          padding: "15px",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0,0,0,0.3)",
          minWidth: "270px",
        }}
      >
        <h3>🚨 Crowd Alert System</h3>

        {crowdZones.map((zone, index) => (
          <div key={index}>
            {zone.risk >= 80 && "🔴"}
            {zone.risk >= 60 &&
              zone.risk < 80 &&
              "🟠"}
            {zone.risk < 60 && "🟢"}

            {" "}
            {zone.name || `Zone ${index + 1}`} : {zone.risk}
          </div>
        ))}

        <hr />

        <h4>Route Details</h4>

        <div>
          Distance : {calculateDistance()} km
        </div>

        <div>
          ETA : {estimateTime()} min
        </div>

        <div>
          Safety Score : {safetyScore()}%
        </div>

        <hr />

        <b>
          {route.length > 0
            ? "✓ Route Generated"
            : "Waiting for Route"}
        </b>

        <br />
        <br />

        <small>
          Auto Refresh: 30 sec
        </small>
      </div>

      {/* MAP */}
      <MapContainer
        center={center}
        zoom={14}
        style={{
          height: "100%",
          width: "100%",
        }}
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <ClickHandler
          source={source}
          destination={destination}
          setSource={setSource}
          setDestination={setDestination}
        />

        {source && (
          <Marker position={source}>
            <Popup>
              <b>Source</b>
            </Popup>
          </Marker>
        )}

        {destination && (
          <Marker position={destination}>
            <Popup>
              <b>Destination</b>
            </Popup>
          </Marker>
        )}

        {route.length > 0 && (
          <Polyline
            positions={route}
            pathOptions={{
              color: "blue",
              weight: 6,
            }}
          />
        )}

        {crowdZones.map((zone, index) => {

          let color = "green";

          if (zone.risk >= 80)
            color = "red";
          else if (zone.risk >= 60)
            color = "orange";

          return (
            <Circle
              key={index}
              center={[zone.lat, zone.lon]}
              radius={zone.risk * 8}
              pathOptions={{
                color,
                fillColor: color,
                fillOpacity: 0.4,
              }}
            >
              <Popup>
                <b>{zone.name}</b>

                <br />

                Risk Score: {zone.risk}
              </Popup>
            </Circle>
          );
        })}
      </MapContainer>
    </div>
  );
}

export default MapView;