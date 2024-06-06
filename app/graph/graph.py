import json
import networkx as nx
import geopandas as gpd
import functools
import math
from flask import g
from ..utils.maps import coords_to_intersection_id, intersection_id_to_coords

def createGraph(priority = "time", step = 0):
  edges = []
  alpha, beta = [2, 1] if priority == "distance" else [1, 2]

  sql = f"""
    SELECT start_node_id, end_node_id, traffic_density, length
    FROM segments AS s
    JOIN roads AS r ON r.id = s.road_id
    JOIN traffic AS t ON t.segment_id = s.id
    WHERE time = {step}
  """
  g.cursor.execute(sql)
  results = g.cursor.fetchall()

  for result in results:
    u = result["start_node_id"]
    v = result["end_node_id"]
    weight = result["length"] * alpha + result["traffic_density"] * beta
    edges.append((u, v, weight))

  G = nx.MultiDiGraph()
  G.add_weighted_edges_from(edges)

  return G