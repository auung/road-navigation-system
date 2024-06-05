from ..graph.GA_vis import GA
from ..graph.graph import createGraph
from .maps import intersection_id_to_node_id

def get_visuals():
  G = createGraph()
  start = intersection_id_to_node_id[6]
  end = intersection_id_to_node_id[104]
  ga = GA(G, start, end)

  all = ga.run()

  return all