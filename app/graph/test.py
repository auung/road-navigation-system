from graph import graph
from GA import GA

G = create_graph()
ga = GA(G, 1, 25)

print(ga.run())