import random
import numpy as np
import networkx as nx


class GA:
  def __init__(self, graph, source, target, population_size=30, generations=300, mutation_rate=0.2, tournament_size=10):
    self.graph = graph
    self.source = source
    self.target = target
    self.population_size = population_size
    self.generations = generations
    self.mutation_rate = mutation_rate
    self.tournament_size = tournament_size
    self.population = self.initialize_population()
    
  def initialize_population(self):
    population = []
    for _ in range(self.population_size):
      individual = self.random_path(self.source, self.target)
      population.append(individual)
    
    return population

  def random_path(self, start, end):
    for _ in range(self.graph.number_of_nodes()):
      path = [start]
      visited = set(path)
      while path[-1] != end:
        current_node = path[-1]
        neighbors = list(self.graph.successors(current_node))
        unvisited_neighbors = [n for n in neighbors if n not in visited]
        if unvisited_neighbors:
          next_node = random.choice(unvisited_neighbors)
          path.append(next_node)
          visited.add(next_node)
        else:
          if len(path) > 1:
            path.pop()
          else:
            break

      if path[-1] == end:
        return path
    return None

  def crossover(self, parent1, parent2):
    start1, end1 = sorted(random.sample(range(len(parent1))[1:-1], k=2))
    start2, end2 = sorted(random.sample(range(len(parent2))[1:-1], k=2))

    print(f"s1: {start1}, e1: {end1}")
    print(f"s2: {start2}, e2: {end2}")

    child1 = parent1[:start1] + parent2[start2:end2] + parent1[end1:]
    child2 = parent2[:start2] + parent1[start1:end1] + parent2[end2:]
    print(f"c1: {child1}")
    print(f"c2: {child2}")
    return self.fix_path(child1), self.fix_path(child2)

  def fix_path(self, path):
    seen = set()
    new_path = []
    for node in path:
      if node in seen:
        continue

      if len(new_path) > 1 and node not in self.graph.successors(new_path[-1]):
        try:
          shortest_path = nx.shortest_path(self.graph, new_path[-1], node)[1:]
          new_path += shortest_path

          for i in shortest_path:
            seen.add(i)

        except nx.NetworkXNoPath:
          return None
      else:
        seen.add(node)
        new_path.append(node)

    return new_path

  def fitness(self, individual):
    if (individual[-1] != self.target):
        return 0
    path_length = sum(self.graph[edge[0]][edge[1]][0]['weight'] for edge in zip(individual[:-1], individual[1:]))
    return 1000 / path_length

  def tournament_selection(self):
    tournament = random.sample(self.population, self.tournament_size)
    tournament_fitness = [self.fitness(individual) for individual in tournament]
    return tournament[np.argmax(tournament_fitness)]

  def run(self):
    p1 = self.tournament_selection()
    p2 = self.tournament_selection()

    child1, child2 = self.crossover(p1, p2)

    print(f"p1: {p1}")
    print(f"p2: {p2}")
    print(f"c1: {child1}")
    print(f"c2: {child2}")

    return [p1, p2]