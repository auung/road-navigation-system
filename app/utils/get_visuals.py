from ..graph.GA_vis import GA
from ..graph.graph import create_graph
from .maps import intersection_id_to_node_id

def get_visuals():
  G = create_graph()
  ga = GA(G, 6, 31)

  all = ga.run()

  return all