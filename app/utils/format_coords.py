from .maps import node_id_to_coords, road_id_to_nodes
from .get_road_segments import get_coords_from_segment
from app import db

def format_route_population(population):
  for ind in population:
    population[population.index(ind)] = [list(reversed(node_id_to_coords[node])) for node in ind]

  return population

def format_route(route):
  cursor = db.connection.cursor()
  formatted_route = []

  for i, (start_node_id, end_node_id) in enumerate(zip(route[:-1], route[1:])):
    sql = f"""
      SELECT road_id
      FROM segments
      WHERE start_node_id={start_node_id} AND end_node_id={end_node_id}
    """
    cursor.execute(sql)
    result = cursor.fetchone()
    road_id = result["road_id"]
    road_coords = road_id_to_nodes[road_id]
    coords = get_coords_from_segment(start_node_id, end_node_id, road_coords)

    if not coords:
      road_coords.reverse()
      coords = get_coords_from_segment(start_node_id, end_node_id, road_coords)

    if i != 0:
      coords = coords[1:]

    for item in coords:
      formatted_route.append(list(reversed(item)))

  return formatted_route