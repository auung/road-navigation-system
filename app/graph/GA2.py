import random
import numpy as np
import networkx as nx


class GA:
  def __init__(self, graph, source, target, population_size=50, generations=300, mutation_rate=0.2, tournament_size=5):
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
    path = [start]

    while path[-1] != end:
      path = [start]

      while path[-1] != end:
        
        neighbors = list(filter(lambda x: x not in path, self.graph.successors(path[-1])))

        if not neighbors:
          break;  # Dead end

        next_node = random.choice(neighbors)

        path.append(next_node)

    return path

  def fitness(self, individual):
    if (individual[-1] != self.target):
        return 0
    path_length = sum(self.graph[edge[0]][edge[1]][0]['weight'] for edge in zip(individual[:-1], individual[1:]))
    return 1000 / path_length

  def run(self):
    result = []

    for individual in self.population:
      result.append({"route": individual, "fitness": self.fitness(individual)})

    result.sort(key=lambda x: x["fitness"], reverse=True)

    for i in result:
      print(i)

    return self.population