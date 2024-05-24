import json
import geopandas as gpd

def read_gpkg(file_location):
	roads = gpd.read_file(file_location, layer="roads", engine="pyogrio", fid_as_index=True)
	roads = roads.to_crs("epsg:4326")
	roads_json = json.loads(gpd.GeoDataFrame.to_json(roads))

	intersections = gpd.read_file(file_location, layer="intersections", engine="pyogrio", fid_as_index=True)
	intersections = intersections.to_crs("epsg:4326")
	intersections_json = json.loads(gpd.GeoDataFrame.to_json(intersections))

	nodes = gpd.read_file(file_location, layer="node", engine="pyogrio", fid_as_index=True)
	nodes = nodes.to_crs("epsg:4326")
	nodes_json = json.loads(gpd.GeoDataFrame.to_json(nodes))

	return {
		"roads": roads_json["features"],
		"intersections": intersections_json["features"],
		"nodes": nodes_json["features"]
	}
