from flask import current_app

road_id_to_nodes = {}
for road in current_app.roads:
  road_id_to_nodes[int(road["id"])] = road["geometry"]["coordinates"]

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

