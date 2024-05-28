from .maps import road_id_to_nodes, node_id_to_coords
from app import db

def get_road_segments(roads, nodes):
  cursor = db.connection.cursor()
  cursor.execute(f"SELECT * FROM segments")
  segments = cursor.fetchall()

  road_segments = []

  for segment in segments:
    id, road_id, start_node_id, end_node_id = segment.values()
    cursor.execute(f"SELECT is_one_way FROM roads WHERE id={road_id}")
    is_one_way = cursor.fetchone()

    road_coords = road_id_to_nodes[road_id]
    nodes = get_coords_from_segment(start_node_id, end_node_id, road_coords)

    if not nodes:
      road_coords.reverse()
      nodes = get_coords_from_segment(start_node_id, end_node_id, road_coords)

    nodes = [list(reversed(node)) for node in nodes]
    cursor.execute(f"SELECT traffic_density FROM traffic WHERE segment_id={id}")
    result = cursor.fetchone()

    road_segments.append({ "id": id, "nodes": nodes, "traffic_density": result["traffic_density"] })

  return road_segments

def get_coords_from_segment(start_node_id, end_node_id, road_coords):
    start_coords = node_id_to_coords[start_node_id]
    end_coords = node_id_to_coords[end_node_id]

    start_idx = road_coords.index(start_coords)
    end_idx = road_coords.index(end_coords)

    return road_coords[start_idx : end_idx + 1]