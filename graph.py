import json
import networkx as nx
import geopandas as gpd
from maps import coords_to_intersection_id, intersection_id_to_coords

roads = gpd.read_file("../geopackage/navigation.gpkg", layer="roads")
roads = roads.to_crs("epsg:4326")
roads_json = json.loads(gpd.GeoDataFrame.to_json(roads))

intersections = gpd.read_file("../geopackage/navigation.gpkg", layer="intersections")
intersections = intersections.to_crs("epsg:4326")
intersections_json = json.loads(gpd.GeoDataFrame.to_json(intersections))

coords_to_id_map = {}
id_to_coords_map = {}

for intersection in intersections_json["features"]:
    id = int(intersection["id"]) + 1
    coords = intersection["geometry"]["coordinates"]
    coords_to_id_map[(coords[1], coords[0])] = id
    id_to_coords_map[id] = [coords[1], coords[0]]

edges = []

for road in roads_json["features"]:
    u_coords = road["geometry"]["coordinates"][0]
    u = coords_to_id_map[(u_coords[1], u_coords[0])]

    v_coords = road["geometry"]["coordinates"][-1]
    v = coords_to_id_map[(v_coords[1], v_coords[0])]

    edges.append((u, v, road["properties"]["road_length"]))

G = nx.Graph()
G.add_weighted_edges_from(edges)

# for edge in G.edges():
#     print(f"edge: {edge}, weight: {G[edge[0]][edge[1]]["weight"]}")

class Graph:
	def __init__(self, roads, intersections, nodes):
		self.roads = roads
		self.intersections = intersections
		self.nodes = nodes

	def getIntersections(self):
		return None

	def create(self):
		edges = []

		for road in self.roads:
			u_coords = road["geometry"]["coordinates"][0]
			u = coords_to_intersection_id[(u_coords[1], u_coords[0])]

			v_coords = road["geometry"]["coordinates"][-1]
			v = coords_to_intersection_id[(v_coords[1], v_coords[0])]

			edges.append((u, v, road["properties"]["road_length"]))

		return nx.MultiDiGraph().add_weighted_edges_from(edges)
