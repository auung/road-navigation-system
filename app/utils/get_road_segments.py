from flask import g
from .maps import road_id_to_coords, node_id_to_coords, coords_to_road_id
import random

def get_road_segments(roads, nodes):
  g.cursor.execute(f"SELECT * FROM segments")
  segments = g.cursor.fetchall()

  road_segments = []
  random_time = random.choice(range(20))

  for segment in segments:
    id, road_id, start_node_id, end_node_id = segment.values()
    g.cursor.execute(f"SELECT is_one_way FROM roads WHERE id={road_id}")
    is_one_way = g.cursor.fetchone()

    road_coords = road_id_to_coords[road_id]
    nodes = get_coords_from_segment(start_node_id, end_node_id, road_coords)

    if not nodes:
      road_coords.reverse()
      nodes = get_coords_from_segment(start_node_id, end_node_id, road_coords)

    nodes = [list(reversed(node)) for node in nodes]
    g.cursor.execute(f"SELECT traffic_density FROM traffic WHERE segment_id={id} AND time={random_time}")
    result = g.cursor.fetchone()

    road_segments.append({ "id": id, "nodes": nodes, "traffic_density": result["traffic_density"] })

  return road_segments

def get_coords_from_segment(start_node_id, end_node_id, road_coords):
    start_coords = node_id_to_coords[start_node_id]
    end_coords = node_id_to_coords[end_node_id]
    start_idx = road_coords.index(start_coords)
    end_idx = road_coords.index(end_coords)

    return road_coords[start_idx : end_idx + 1]