from ..graph.GA import GA
from ..graph.graph import createGraph
from .maps import intersection_id_to_node_id
from .format_coords import format_route, get_distance
import math, random

def get_route(start, end):
  start = intersection_id_to_node_id[start]
  end = intersection_id_to_node_id[end]

  random_time = random.choice(range(20))
  G = createGraph(random_time)
  ga = GA(G, start, end)
  best = ga.run()

  distance = round(get_distance(best))
  time = f"{math.ceil(distance / 32000 * 60)} min"
  distance = f"{round(distance / 1000, 1)} km" if len(str(distance)) > 3 else f"{distance} m"

  route = format_route(best)

  return route, f"{distance} | {time}"