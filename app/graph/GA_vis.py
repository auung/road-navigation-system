import random
import numpy as np
import networkx as nx
import gc
from ..utils.format_coords import format_route


class GA:
  def __init__(self, graph, source, target, population_size=25, generations=300, mutation_rate=0.25, tournament_size=15):
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

  def random_path_random(self, start, end):
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

  def random_path_backtrack(self, start, end):
    for _ in range(self.graph.number_of_nodes()):
      path = [start]
      visited = set(path)

      while path[-1] != end:
        current_node = path[-1]
        neighbors = list(filter(lambda x: x not in visited, self.graph.successors(current_node)))
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

  def random_path(self, start, end):
    return self.random_path_backtrack(start, end)

  def fitness(self, individual):
    if (individual[-1] != self.target):
      return 0
    path_length = sum(self.graph[edge[0]][edge[1]][0]['weight'] for edge in zip(individual[:-1], individual[1:]))
    return 10 / path_length

  def tournament_selection(self):
    tournament = random.sample(self.population, self.tournament_size)
    tournament_fitness = [self.fitness(individual) for individual in tournament]
    return tournament[np.argmax(tournament_fitness)]

  def crossover(self, parent1, parent2):
    start1, end1 = sorted(random.sample(range(len(parent1))[1:-1], k=2))
    start2, end2 = sorted(random.sample(range(len(parent2))[1:-1], k=2))

    child1 = parent1[:start1] + parent2[start2:end2] + parent1[end1:]
    child2 = parent2[:start2] + parent1[start1:end1] + parent2[end2:]

    start = random.choice(range(len(parent1)))
    child = parent1[:start] + parent2[start:]
    return self.fix_path(child)

  def fix_path(self, path):
    seen = set()
    new_path = []
    for node in path:
      if node in seen:
        break

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

  def mutate(self, individual):
    if len(individual) > 2 and random.random() < self.mutation_rate:
      node = random.choice(range(len(individual))[1:-1])
      individual = individual[:node] + self.random_path_random(individual[node], self.target)

    return individual

  def run(self):
    gc.disable()
    all = []
    best_individual = None
    best_fitness = float('-inf')

    for generation in range(self.generations):
      sorted_population = sorted(self.population, key=lambda x: self.fitness(x))
      all.append([{"route": format_route(route), "distance": 0} for route in sorted_population])
      new_population = []

      while len(new_population) < self.population_size:
        best1 = self.tournament_selection()
        best2 = self.tournament_selection()
        child1 = self.crossover(best1, best2)
        child2 = self.crossover(best2, best1)

        new_population.append(best1)
        new_population.append(best2)

        if len(child1) > 2:
          child1 = self.mutate(child1)
        if len(child2) > 2:
          child2 = self.mutate(child2)

        new_population.append(child1)
        new_population.append(child2)

      self.population = new_population

      for individual in self.population:
        current_fitness = self.fitness(individual)
        if current_fitness > best_fitness:
          best_fitness = current_fitness
          best_individual = individual

      # print(f"Generation {generation + 1}: Best path = {best_individual}, Best Fitness = {best_fitness}")

    # path_length = sum(self.graph[edge[0]][edge[1]]['weight'] for edge in zip(best_individual[:-1], best_individual[1:]))
    gc.enable()
    return all
