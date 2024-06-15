import json
import networkx as nx
import geopandas as gpd
import functools
import math
from flask import g, current_app
from ..utils.maps import coords_to_intersection_id, road_id_to_coords, coords_to_node_id

def get_edge_from_coords(coords_list, step):
  u = coords_to_intersection_id[tuple(coords_list[0])]
  v = coords_to_intersection_id[tuple(coords_list[-1])]

  nodes = []
  for coords in coords_list:
    try:
      nodes.append(coords_to_node_id[tuple(coords)])
    except KeyError:
      pass

  total_density = 0
  for start_node_id, end_node_id in zip(nodes[:-1], nodes[1:]):
    g.cursor.execute(f"""
      SELECT traffic_density
      FROM segments AS s
      JOIN roads AS r ON r.id = s.road_iD
      JOIN traffic AS t ON t.segment_id = s.id
      WHERE start_node_id = {start_node_id} AND end_node_id = {end_node_id} AND time = {step}
    """)
    result = g.cursor.fetchone()
    total_density += result["traffic_density"]

  return u, v, total_density

def create_graph(priority = "time", step = 0):
  edges = []
  alpha, beta = [1, 0] if priority == "distance" else [0, 1]
  roads = current_app.roads

  for road in roads:
    road_id = int(road["id"])
    coords_list = road_id_to_coords[road_id]

    u, v, traffic_density = get_edge_from_coords(coords_list, step)
    weight = (alpha * road["properties"]["road_length"]) + (beta * traffic_density)

    edges.append((u, v, weight))

    if not road["properties"]["is_one_way"]:
      coords_list.reverse()
      u, v, traffic_density = get_edge_from_coords(coords_list, step)
      weight = (alpha * road["properties"]["road_length"]) + (beta * traffic_density)

      edges.append((u, v, weight))

  G = nx.MultiDiGraph()
  G.add_weighted_edges_from(edges)

  return G