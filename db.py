from pathlib import Path
import mysql.connector
import json
import geopandas as gpd
import random


class Database:
  def __init__(self, db_name):
    self.db_name = db_name
    self.conn = mysql.connector.connect(
      user='root',
      password='',
      host='127.0.0.1'
    )
    self.cursor = self.conn.cursor(dictionary=True)
    self.roads, self.intersections, self.nodes = self.read_gpkg(Path("geopackage\\navigation.gpkg").absolute())
    self.coords_to_node_id = {}
    self.get_mapping()


  def get_mapping(self):
    for node in self.nodes:
      coords = node["geometry"]["coordinates"]
      self.coords_to_node_id[(coords[0], coords[1])] = int(node["id"])

  def read_gpkg(self, file_location):
    roads = gpd.read_file(file_location, layer="roads", engine="pyogrio", fid_as_index=True)
    roads = roads.to_crs("epsg:4326")
    roads_json = json.loads(gpd.GeoDataFrame.to_json(roads))

    intersections = gpd.read_file(file_location, layer="intersections", engine="pyogrio", fid_as_index=True)
    intersections = intersections.to_crs("epsg:4326")
    intersections_json = json.loads(gpd.GeoDataFrame.to_json(intersections))

    nodes = gpd.read_file(file_location, layer="node", engine="pyogrio", fid_as_index=True)
    nodes = nodes.to_crs("epsg:4326")
    nodes_json = json.loads(gpd.GeoDataFrame.to_json(nodes))

    return roads_json["features"], intersections_json["features"], nodes_json["features"]


  def get_segments(self, edge_coords, node_coords):
    segments = []
    
    x = edge_coords[0]
    y = None

    for coord in edge_coords[1:-1]:
      if coord in node_coords:
        y = coord
        segments.append([x, y])
        x = coord
      
    y = edge_coords[-1]
    segments.append([x, y])

    return segments


  def insert_roads(self):
    # self.cursor.execute("ALTER TABLE roads SET AUTO_INCREMENT = 1")
    for road in self.roads:
      id = int(road["id"])
      length = float(road["properties"]["road_length"])
      is_one_way = road["properties"]["is_one_way"]

      sql = f"""
        INSERT INTO roads (id, length, is_one_way) VALUES ({id}, {length}, {is_one_way})
        ON DUPLICATE KEY UPDATE length={length}, is_one_way={is_one_way};
      """

      self.cursor.execute(sql)

    self.conn.commit()


  def insert_segments(self):
    node_coords = [node["geometry"]["coordinates"] for node in self.nodes]

    for road in self.roads:
      segments = self.get_segments(road["geometry"]["coordinates"], node_coords)
      road_id = int(road["id"])
      is_one_way = road["properties"]["is_one_way"]

      for segment in segments:
        start_node_id = self.coords_to_node_id[tuple(segment[0])]
        end_node_id = self.coords_to_node_id[tuple(segment[1])]

        sql = f"""
          INSERT INTO segments (id, road_id, start_node_id, end_node_id) VALUES (NULL, {road_id}, {start_node_id}, {end_node_id})
        """

        self.cursor.execute(sql)

        if not is_one_way:
          start_node_id = self.coords_to_node_id[tuple(segment[1])]
          end_node_id = self.coords_to_node_id[tuple(segment[0])]
          
          sql = f"""
            INSERT INTO segments (id, road_id, start_node_id, end_node_id) VALUES (NULL, {road_id}, {start_node_id}, {end_node_id})
          """
          
          self.cursor.execute(sql)

    self.conn.commit()

  
  def insert_traffic(self):
    sql = "SELECT id FROM segments"
    self.cursor.execute(sql)
    segments = self.cursor.fetchall()

    for i in range(10):
      for segment in segments:
        segment_id = segment["id"]

        traffic_density = round(random.triangular(0, 100, 15)) / 100
        sql = f"INSERT INTO traffic (id, segment_id, traffic_density, time) VALUES (NULL, {segment_id}, {traffic_density}, {i + 1})"
        self.cursor.execute(sql)

    self.conn.commit()


  def create_db(self):
    self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}`;")
    self.cursor.execute(f"USE `{self.db_name}`;")
    print("DB created successfully")
    

  def delete_tables(self):
    self.cursor.execute("DROP TABLE `roads`")
    self.cursor.execute("DROP TABLE `segments`")
    self.cursor.execute("DROP TABLE `traffic`")


  def create_tables(self):
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS `roads` (
        `id` INT(11) NOT NULL AUTO_INCREMENT,
        `length` FLOAT NOT NULL,
        `is_one_way` BOOLEAN NOT NULL DEFAULT 0,
        PRIMARY KEY (`id`)
      );
    """)
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS `segments` (
        `id` INT(11) NOT NULL AUTO_INCREMENT,
        `road_id` INT(11) NOT NULL,
        `start_node_id` INT(11) NOT NULL,
        `end_node_id` INT(11) NOT NULL,
        PRIMARY KEY (`id`)
      );
    """)
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS `traffic` (
        `id` INT(11) NOT NULL AUTO_INCREMENT,
        `segment_id` INT(11) NOT NULL,
        `traffic_density` float NOT NULL,
        `time` INT(11) NOT NULL,
        PRIMARY KEY (`id`)
      );
    """)
    print("Tables created successfully")


  def create(self):
    self.create_db()
    self.delete_tables()
    self.create_tables()
    self.insert_roads()
    self.insert_segments()
    self.insert_traffic()

    self.cursor.close()
    self.conn.close()
    
    print("db created and data inserted")
