from ..graph.GA import GA
from ..graph.graph import createGraph
from .maps import intersection_id_to_node_id, coords_to_road_id, intersection_id_to_coords
from .format_coords import format_route, get_distance
from .get_intersections import get_intersetions_from_route
from flask import g
import math, random

def get_max_speed(road_id, time):
  sql = f"""
    SELECT r.id, length, is_one_way, COUNT(s.id) AS count, SUM(traffic_density) AS traffic_density
    FROM roads AS r
    JOIN segments AS s ON s.road_id = r.id
    JOIN traffic AS t ON t.segment_id = s.id
    WHERE r.id = {road_id} AND t.time = {time}
  """
  g.cursor.execute(sql)
  result = g.cursor.fetchone()

  if not result["is_one_way"]:
    result["count"] = round(result["count"] / 2)

  length = result["length"]
  count = result["count"]
  density = result["traffic_density"]

  percent = count / density * 100

  if 0 >= percent > 25:
    speed = 40

  elif 25 >= percent > 50:
    speed = 30

  elif 50 >= percent > 75:
    speed = 20

  else:
    speed = 10

  return speed, length

def get_road_ids(route):
  intersections = get_intersetions_from_route(route)
  road_id_list = []

  for start_id, end_id in zip(intersections[:-1], intersections[1:]):
    start_coord = tuple(reversed(intersection_id_to_coords[start_id]))
    end_coord = tuple(reversed(intersection_id_to_coords[end_id]))

    try:
      road_id = coords_to_road_id[(start_coord, end_coord)]
    except KeyError:
      road_id = coords_to_road_id[(end_coord, start_coord)]

    road_id_list.append(road_id)

  return road_id_list
  

def calc_travel_time(road_id, time):
  adjusted_speed_kmh, length_m = get_max_speed(road_id, time)

  length_km = length_m / 1000
  
  time_hours = length_km / adjusted_speed_kmh

  time_minutes = time_hours * 60
  
  return time_minutes


def get_route(start, end, priority):
  start = intersection_id_to_node_id[start]
  end = intersection_id_to_node_id[end]

  random_time = random.choice(range(20))
  G = createGraph(priority, random_time)
  ga = GA(G, start, end)
  best = ga.run()

  time = 0

  for road_id in get_road_ids(best):
    time += calc_travel_time(road_id, random_time)

  distance = round(get_distance(best))
  time = f"{round(time)} min"
  distance = f"{round(distance / 1000, 1)} km" if len(str(distance)) > 3 else f"{distance} m"

  route = format_route(best)

  return route, f"{distance} | {time}"