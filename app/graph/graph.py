import json
import networkx as nx
import geopandas as gpd
import functools
from maps import coords_to_intersection_id, intersection_id_to_coords
from app import mysql

class Graph:
  def __init__(self, roads, intersections, nodes):
    self.roads = roads
    self.intersections = intersections
    self.nodes = nodes

  def getIntersections(self):
    return None

  def getEdge(coords):
    u_coords = coords[0]
    u = coords_to_intersection_id[(u_coords[1], u_coords[0])]

    v_coords = coords[-1]
    v = coords_to_intersection_id[(v_coords[1], v_coords[0])]

  def create(self):
    edges = []

    sql = f"""
      SELECT start_node_id, end_node_id, traffic_density, length
      FROM segments AS s
      JOIN roads AS r ON r.id = s.road_id
      JOIN traffic AS t ON t.segment_id = s.id
    """

    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    for result in results:
      u = result["start_node_id"]
      v = result["end_node_id"]
      weight = result["traffic_density"] * result["length"]
      edges.append((u, v, weight))

    G = nx.MultiDiGraph()
    G.add_weighted_edges_from(edges)

    return G