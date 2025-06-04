# import random
# import numpy as np
#
#
# def initialize_population(pop_size, chrom_length, ones_count):
#     population = []
#     for _ in range(pop_size):
#         chrom = [0] * chrom_length
#         ones_indices = random.sample(range(chrom_length), ones_count)
#         for idx in ones_indices:
#             chrom[idx] = 1
#         population.append(chrom)
#     return population
#
#
# def fitness(chromosome, exposure_values):
#     return sum(chromosome[i] * exposure_values[i] for i in range(len(chromosome)))
#
#
# def tournament_selection(population, exposure_values, tournament_size=3):
#     tournament = random.sample(population, tournament_size)
#     return max(tournament, key=lambda chrom: fitness(chrom, exposure_values))
#
#
# def two_point_crossover(parent1, parent2, ones_count):
#     length = len(parent1)
#     point1, point2 = sorted(random.sample(range(length), 2))
#     child1, child2 = parent1[:], parent2[:]
#
#     # Perform two-point crossover
#     child1[point1:point2], child2[point1:point2] = parent2[point1:point2], parent1[point1:point2]
#
#     # Ensure exactly 5 ones in each child
#     for child in [child1, child2]:
#         ones = sum(child)
#         if ones > ones_count:
#             ones_indices = [i for i, x in enumerate(child) if x == 1]
#             for _ in range(ones - ones_count):
#                 idx = random.choice(ones_indices)
#                 child[idx] = 0
#                 ones_indices.remove(idx)
#         elif ones < ones_count:
#             zeros_indices = [i for i, x in enumerate(child) if x == 0]
#             for _ in range(ones_count - ones):
#                 idx = random.choice(zeros_indices)
#                 child[idx] = 1
#                 zeros_indices.remove(idx)
#
#     return child1, child2
#
#
# def mutation(chromosome, ones_count):
#     chrom = chromosome[:]
#     ones_indices = [i for i, x in enumerate(chrom) if x == 1]
#     zeros_indices = [i for i, x in enumerate(chrom) if x == 0]
#     if ones_indices and zeros_indices:
#         one_idx = random.choice(ones_indices)
#         zero_idx = random.choice(zeros_indices)
#         chrom[one_idx], chrom[zero_idx] = 0, 1
#     return chrom
#
#
# def genetic_algorithm(exposure_values, pop_size=10, generations=20, ones_count=5):
#     chrom_length = len(exposure_values)
#     population = initialize_population(pop_size, chrom_length, ones_count)
#
#     for _ in range(generations):
#         new_population = []
#
#         # Elitism: keep the best chromosome
#         best_chrom = max(population, key=lambda chrom: fitness(chrom, exposure_values))
#         new_population.append(best_chrom)
#
#         # Generate new population
#         while len(new_population) < pop_size:
#             parent1 = tournament_selection(population, exposure_values)
#             parent2 = tournament_selection(population, exposure_values)
#             child1, child2 = two_point_crossover(parent1, parent2, ones_count)
#
#             # Apply mutation with probability 0.1
#             if random.random() < 0.1:
#                 child1 = mutation(child1, ones_count)
#             if random.random() < 0.1:
#                 child2 = mutation(child2, ones_count)
#
#             new_population.extend([child1, child2])
#
#         population = new_population[:pop_size]
#
#     best_chrom = max(population, key=lambda chrom: fitness(chrom, exposure_values))
#     best_fitness = fitness(best_chrom, exposure_values)
#     return best_chrom, best_fitness
#
#
# def main() -> None:
#     # Example usage
#     exposure_values = [4, 8, 2, 7, 3, 9, 1, 6, 5, 10]
#     best_chromosome, best_fitness = genetic_algorithm(exposure_values)
#     print(f"Best chromosome: {best_chromosome}")
#     print(f"Total exposure: {best_fitness}")
#
#
# if __name__ == "__main__":
#     main()
#
import random


def fitness(chromosome, exposure_values):
    return sum(chromosome[i] * exposure_values[i] for i in range(len(chromosome)))


def initPopulation(pop_size, chrom_length, ones_count) -> list:
    population = []
    for _ in range(pop_size):
        chrom = [0] * chrom_length
        ones_indices = random.sample(range(chrom_length), ones_count)
        for i in ones_indices:
            chrom[i] = 1
        population.append(chrom)
    return population


def tournamentSelection(population, exposure_values):
    tournament = random.sample(population, 2)
    return max(tournament, key=lambda chrom: fitness(chrom, exposure_values))


def singlePointCrossover(parent1, parent2, ones_count):
    length = len(parent1)
    point = random.randint(1, length - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    for child in [child1, child2]:
        ones = sum(child)
        if ones > ones_count:
            ones_indices = [i for i, x in enumerate(child) if x == 1]
            for _ in range(ones - ones_count):
                idx = random.choice(ones_indices)
                child[idx] = 0
                ones_indices.remove(idx)
        elif ones < ones_count:
            zeros_indices = [i for i, x in enumerate(child) if x == 0]
            for _ in range(ones_count - ones):
                idx = random.choice(zeros_indices)
                child[idx] = 1
                zeros_indices.remove(idx)
    return child1, child2


def mutation(chromosome, ones_count):
    chrom = chromosome[:]
    ones_indices = [i for i, x in enumerate(chrom) if x == 1]
    zeros_indices = [i for i, x in enumerate(chrom) if x == 0]
    if ones_indices and zeros_indices:
        one_idx = random.choice(ones_indices)
        zero_idx = random.choice(zeros_indices)
        chrom[one_idx], chrom[zero_idx] = 0, 1
    return chrom


def geneticAlgorithm(exposure_values, pop_size=6, generations=10, ones_count=5):
    chrom_length = len(exposure_values)
    population = initPopulation(pop_size, chrom_length, ones_count)

    for _ in range(generations):
        new_population = []
        best_chrom = max(population, key=lambda chrom: fitness(chrom, exposure_values))
        new_population.append(best_chrom)  # حفظ بهترین

        while len(new_population) < pop_size:
            parent1 = tournamentSelection(population, exposure_values)
            parent2 = tournamentSelection(population, exposure_values)
            child1, child2 = singlePointCrossover(parent1, parent2, ones_count)

            if random.random() < 0.1:
                child1 = mutation(child1, ones_count)
                child2 = mutation(child2, ones_count)

            new_population.extend([child1, child2])

        population = new_population[:pop_size]

    best_chrom = max(population, key=lambda chrom: fitness(chrom, exposure_values))
    best_fitness = fitness(best_chrom, exposure_values)
    return best_chrom, best_fitness


def main() -> None:
    exposure_values = [3, 7, 1, 6, 2, 8, 4, 5, 9, 10]
    best_chromosome, best_fitness = geneticAlgorithm(exposure_values)
    print(f"Best Chromosome: {best_chromosome}")
    print(f"مجموع نوردهی: {best_fitness}")


if __name__ == "__main__":
    main()
