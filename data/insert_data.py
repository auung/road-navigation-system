import json
import mysql.connector
from geopandas import gpd
from road_direction import one_way_roads

roads = gpd.read_file("./geopackage/navigation.gpkg", layer="roads", engine='pyogrio', fid_as_index=True)
roads = roads.to_crs("epsg:4326")
roads_json = json.loads(gpd.GeoDataFrame.to_json(roads))

intersections = gpd.read_file("./geopackage/navigation.gpkg", layer="intersections", engine='pyogrio', fid_as_index=True)
intersections = intersections.to_crs("epsg:4326")
intersections_json = json.loads(gpd.GeoDataFrame.to_json(intersections))

nodes = gpd.read_file("./geopackage/navigation.gpkg", layer="node", engine='pyogrio', fid_as_index=True)
nodes = nodes.to_crs("epsg:4326")
nodes_json = json.loads(gpd.GeoDataFrame.to_json(nodes))
node_coords = [node["geometry"]["coordinates"] for node in nodes_json["features"]]

coords_to_node = {}

for node in nodes_json["features"]:
  x = node["geometry"]["coordinates"][0]
  y = node["geometry"]["coordinates"][1]
  id = int(node["id"])
  coords_to_node[(x, y)] = id

cnx = mysql.connector.connect(
  user='root',
  password='',
  host='127.0.0.1',
  database='86_akk_crp'
)

cursor = cnx.cursor()


def get_segments(edge, node_coords):
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

  return segments


def insert_roads():
  for road in roads_json["features"]:
    id = int(road["id"])
    length = float(road["properties"]["road_length"])
    is_one_way = road["properties"]["is_one_way"]

    sql = f"""
      INSERT INTO roads (id, length, is_one_way) VALUES ({id}, {length}, {is_one_way})
      ON DUPLICATE KEY UPDATE length={length}, is_one_way={is_one_way};
    """

    cursor.execute(sql)

def insert_segments():
  for road in roads_json["features"]:
    segments = get_segments(road, node_coords)
    road_id = int(road["id"])
    is_one_way = road["properties"]["is_one_way"]

    for segment in segments:
      start_node_id = coords_to_node[tuple(segment[0])]
      end_node_id = coords_to_node[tuple(segment[1])]

      sql = f"""
        INSERT INTO segments (id, road_id, start_node_id, end_node_id) VALUES (NULL, {road_id}, {start_node_id}, {end_node_id})
        ON DUPLICATE KEY UPDATE road_id={road_id}, start_node_id={start_node_id}, end_node_id={end_node_id};
      """

      cursor.execute(sql)

      if not is_one_way:
        start_node_id = coords_to_node[tuple(segment[1])]
        end_node_id = coords_to_node[tuple(segment[0])]
        
        sql = f"""
          INSERT INTO segments (id, road_id, start_node_id, end_node_id) VALUES (NULL, {road_id}, {start_node_id}, {end_node_id})
          ON DUPLICATE KEY UPDATE road_id={road_id}, start_node_id={start_node_id}, end_node_id={end_node_id};
        """
        
        cursor.execute(sql)

insert_segments()

cnx.commit()
cursor.close()
cnx.close()