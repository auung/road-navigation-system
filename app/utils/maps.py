from flask import current_app

road_id_to_coords = {}
coords_to_road_id = {}
coords_to_distance = {}

for road in current_app.roads:
  coords = road["geometry"]["coordinates"]
  start_end_coords = [coords[0], coords[-1]]
  road_id_to_coords[int(road["id"])] = coords
  coords_to_road_id[(tuple(start_end_coords[0]), tuple(start_end_coords[1]))] = int(road["id"])
  coords_to_distance[(tuple(start_end_coords[0]), tuple(start_end_coords[1]))] = road["properties"]["road_length"]

node_id_to_coords = {}
coords_to_node_id = {}
for node in current_app.nodes:
  coords = node["geometry"]["coordinates"]
  node_id_to_coords[int(node["id"])] = coords
  coords_to_node_id[(coords[0], coords[1])] = int(node["id"])

coords_to_intersection_id = {}
intersection_id_to_coords = {}
intersection_id_to_node_id = {}

for intersection in current_app.intersections:
  
  id = int(intersection["id"])
  coords = intersection["geometry"]["coordinates"]
  coords_to_intersection_id[(coords[1], coords[0])] = id
  intersection_id_to_coords[id] = [coords[1], coords[0]]
  intersection_id_to_node_id[id] = coords_to_node_id[(coords[0], coords[1])]
  