import random
import numpy as np
import networkx as nx


class GA:
  def __init__(self, graph, source, target, population_size=30, generations=300, mutation_rate=0.3, tournament_size=5):
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

    return []

  def fitness(self, individual):
    if (individual[-1] != self.target):
      return 0
    path_length = sum(self.graph[edge[0]][edge[1]][0]['weight'] for edge in zip(individual[:-1], individual[1:]))
    return 10 / path_length

  def roulette_wheel_selection(self, population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [fitness / total_fitness for fitness in fitnesses]
    selected_index = np.random.choice(range(len(population)), p=selection_probs)

    return population[selected_index]

  def tournament_selection(self):
    tournament = random.sample(self.population, self.tournament_size)
    tournament_fitness = [self.fitness(individual) for individual in tournament]
    
    return self.roulette_wheel_selection(tournament, tournament_fitness)

  def crossover(self, parent1, parent2):
    min_length = sorted([len(parent1), len(parent2)])[0]
    start, end = sorted(random.sample(range(min_length)[1:-1], k=2))

    child = parent1[:start] + parent2[start:end] + parent1[end:]

    return self.fix_path(child)

  def optimize_path(self, path):
    new_path = []
    i = 0

    while i < len(path):
      successors = self.graph.successors(path[i])
      new_node = path[i]
      
      for j in range(i + 2, len(path)):
        if path[j] in successors:
          i = j
          break

        if path[i] == path[j]:
          i = j + 1
          new_node = path[j]
          break
      else:
        i += 1
        
      new_path.append(new_node)
    return new_path

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
          return []
      else:
        seen.add(node)
        new_path.append(node)

    return self.optimize_path(new_path)

  def mutate(self, individual):
    if len(individual) > 2 and random.random() < self.mutation_rate:
      node = random.choice(range(len(individual))[:-1])
      local_target = random.choice(range(len(individual))[node:])
      individual = individual[:node] + self.random_path(individual[node], individual[local_target]) + individual[local_target + 1:]

    return individual

  def run(self):
    best_individual = None
    best_fitness = float('-inf')

    for generation in range(self.generations):
      new_population = []
      new_population.append(sorted(self.population, key=lambda x: self.fitness(x))[-1])

      while len(new_population) < self.population_size:
        best1 = self.tournament_selection()
        best2 = self.tournament_selection()
        child = self.crossover(best1, best2)

        if len(child) > 2:
          child = self.mutate(child)

          if child:
            new_population.append(child)

        new_population.append(best1)
        new_population.append(best2)

      self.population = new_population

      for individual in self.population:
        current_fitness = self.fitness(individual)
        if current_fitness > best_fitness:
          best_fitness = current_fitness
          best_individual = individual

      # print(f"Generation {generation + 1}: Best path = {best_individual}, Best Fitness = {best_fitness}")

    return best_individual, best_fitness
