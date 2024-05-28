from ..graph.GA import GA
from ..graph.graph import createGraph
from .maps import intersection_id_to_node_id
from .format_coords import format_route

def get_route(start, end):
  start = intersection_id_to_node_id[start]
  end = intersection_id_to_node_id[end]

  G = createGraph()
  ga = GA(G, start, end)
  best = ga.run()

  return format_route(best)