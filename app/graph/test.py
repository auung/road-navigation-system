from graph import graph
from GA import GA

G = createGraph()
ga = GA(G, 1, 25)

print(ga.run())