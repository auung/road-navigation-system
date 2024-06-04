from flask import current_app
from .maps import intersection_id_to_node_id as map

def get_intersections():
  intersections = []

  for intersection in current_app.intersections:
    intersections.append({
      "id": intersection["id"],
      "coords": [
        intersection["geometry"]["coordinates"][1],
        intersection["geometry"]["coordinates"][0]
      ]
    })

  return intersections

def get_intersetions_from_route(route):
  intersection_route = []
  for node_id in route:
    try:
      intersection_route.append(list(map.keys())[list(map.values()).index(node_id)])
    except ValueError:
      pass
  
  return intersection_route