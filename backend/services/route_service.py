import osmnx as ox
import networkx as nx
import math

print("Loading road network...")

graph = ox.graph_from_point(
    (13.0215, 80.1670),
    dist=6000,
    network_type="drive"
)

print("Road network loaded")

# (latitude, longitude, crowd risk)
crowd_zones = [
    (13.0215, 80.1670, 97.84),  # High risk
    (13.0290, 80.1710, 70.00),  # Medium risk
    (13.0150, 80.1600, 20.00)   # Low risk
]


def get_crowd_risk(lat, lon):

    max_risk = 0

    for cz_lat, cz_lon, risk in crowd_zones:

        distance = math.sqrt(
            (lat - cz_lat) ** 2 +
            (lon - cz_lon) ** 2
        )

        # radius of influence
        radius = 0.002

        if distance < radius:

            # stronger risk near center
            adjusted_risk = risk * (1 - distance / radius)

            if adjusted_risk > max_risk:
                max_risk = adjusted_risk

    return max_risk


def crowd_weight(u, v, data):

    base_length = data.get("length", 1)

    lat = graph.nodes[v]["y"]
    lon = graph.nodes[v]["x"]

    risk = get_crowd_risk(lat, lon)

    # Balanced routing:
    # distance remains dominant
    # crowd risk slightly influences path

    penalty_factor = 1 + (risk / 50)

    return base_length * penalty_factor


def find_route(start_lat, start_lon, end_lat, end_lon):

    start_node = ox.distance.nearest_nodes(
        graph,
        start_lon,
        start_lat
    )

    end_node = ox.distance.nearest_nodes(
        graph,
        end_lon,
        end_lat
    )

    route = nx.astar_path(
        graph,
        start_node,
        end_node,
        weight=crowd_weight
    )

    route_edges = ox.routing.route_to_gdf(graph, route)

    coordinates = []

    for _, edge in route_edges.iterrows():

        if edge.geometry is not None:

            for lon, lat in edge.geometry.coords:
                coordinates.append([lat, lon])

    return coordinates