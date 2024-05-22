from graph import G
from GA import GA

ga = GA(G, 68, 23)
best = ga.run()

print(best)