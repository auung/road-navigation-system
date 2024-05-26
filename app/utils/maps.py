from . import read_gpkg
from flask import current_app

road_id_to_nodes = {}
for road in current_app.roads:
  road_id_to_nodes[int(road["id"])] = road["geometry"]["coordinates"]

node_id_to_coords = {}
for node in current_app.nodes:
  node_id_to_coords[int(node["id"])] = node["geometry"]["coordinates"]

coords_to_intersection_id = {}
intersection_id_to_coords = {}

for intersection in current_app.intersections:
  id = int(intersection["id"])
  coords = intersection["geometry"]["coordinates"]
  coords_to_intersection_id[(coords[1], coords[0])] = id
  intersection_id_to_coords[id] = [coords[1], coords[0]]
