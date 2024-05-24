import mysql.connector
from geopandas import gpd
from maps import road_id_to_nodes, node_id_to_coords
import json

def get_road_segments(roads, nodes):
  cnx = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
    database='86_akk_crp'
  )
  cursor = cnx.cursor()

  cursor.execute(f"SELECT * FROM segments")
  segments = cursor.fetchall()

  road_segments = []

  for (id, road_id, start_node_id, end_node_id) in segments:
    cursor.execute(f"SELECT is_one_way FROM roads WHERE id={road_id}")
    is_one_way = cursor.fetchone()[0]

    start_coords = node_id_to_coords[start_node_id]
    end_coords = node_id_to_coords[end_node_id]

    road_coords = road_id_to_nodes[road_id]

    start_idx = road_coords.index(start_coords)
    end_idx = road_coords.index(end_coords)

    nodes = road_coords[start_idx : end_idx + 1]

    if not nodes:
      road_coords.reverse()
      start_idx = road_coords.index(start_coords)
      end_idx = road_coords.index(end_coords)

      nodes = road_coords[start_idx : end_idx + 1]

    nodes = [list(reversed(node)) for node in nodes]
    cursor.execute(f"SELECT traffic_density FROM traffic WHERE segment_id={id}")
    traffic_density = cursor.fetchone()[0]

    road_segments.append({ "id": id, "nodes": nodes, "traffic_density": traffic_density })

  cursor.close()
  cnx.close()

  return road_segments

# roads = gpd.read_file("./geopackage/navigation.gpkg", layer="roads", engine="pyogrio", fid_as_index=True)
# roads = roads.to_crs("epsg:4326")
# roads = json.loads(gpd.GeoDataFrame.to_json(roads))["features"]

# nodes = gpd.read_file("./geopackage/navigation.gpkg", layer="node", engine="pyogrio", fid_as_index=True)
# nodes = nodes.to_crs("epsg:4326")
# nodes = json.loads(gpd.GeoDataFrame.to_json(nodes))["features"]

# get_road_segments(roads, nodes)