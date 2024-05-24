from read_gpkg import read_gpkg

gpkg = read_gpkg("./geopackage/navigation.gpkg")

roads = gpkg["roads"]
intersections = gpkg["intersections"]
nodes = gpkg["nodes"]

road_id_to_nodes = {}
for road in roads:
  road_id_to_nodes[int(road["id"])] = road["geometry"]["coordinates"]

node_id_to_coords = {}
for node in nodes:
  node_id_to_coords[int(node["id"])] = node["geometry"]["coordinates"]

coords_to_intersection_id = {}
intersection_id_to_coords = {}

for intersection in intersections:
  id = int(intersection["id"])
  coords = intersection["geometry"]["coordinates"]
  coords_to_intersection_id[(coords[1], coords[0])] = id
  intersection_id_to_coords[id] = [coords[1], coords[0]]
