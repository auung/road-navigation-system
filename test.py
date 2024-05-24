import geopandas as gpd
import json

nodes = gpd.read_file("./geopackage/navigation.gpkg", layer="node_test")
nodes = nodes.to_crs("epsg:4326")
nodes_json = json.loads(gpd.GeoDataFrame.to_json(nodes))

edges = gpd.read_file("./geopackage/navigation.gpkg", layer="edge_test")
edges = edges.to_crs("epsg:4326")
edges_json = json.loads(gpd.GeoDataFrame.to_json(edges))

node_coords = [node["geometry"]["coordinates"] for node in nodes_json["features"]]

for edge in edges_json["features"]:
  coords = edge["geometry"]["coordinates"]
  segments = []

  x = coords[0]
  y = None

  for coord in coords[1:-1]:
    if coord in node_coords:
      y = coord
      segments.append([x, y])
      x = coord
    
  y = coords[-1]
  segments.append([x, y])

for i in segments:
  print(i)
    






