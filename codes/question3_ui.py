import random
import copy


def create_initial_population(pop_size, genome_length, n_ones):
    population = []
    for _ in range(pop_size):
        individual = [0] * genome_length
        ones_indices = random.sample(range(genome_length), n_ones)
        for idx in ones_indices:
            individual[idx] = 1
        population.append(individual)
    return population


def calculate_fitness(individual, exposures):
    return sum(bit * exposures[i] for i, bit in enumerate(individual))


def tournament_selection(population, exposures, k=3):
    contenders = random.sample(population, k)
    return max(contenders, key=lambda ind: calculate_fitness(ind, exposures))


def repair(child):
    while sum(child) > n_ones:
        i = random.choice([i for i, b in enumerate(child) if b == 1])
        child[i] = 0
    while sum(child) < n_ones:
        i = random.choice([i for i, b in enumerate(child) if b == 0])
        child[i] = 1


def crossover(parent1, parent2, n_ones=5):
    length = len(parent1)
    child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
    p1, p2 = sorted(random.sample(range(1, length-1), 2))
    child1[p1:p2], child2[p1:p2] = parent2[p1:p2], parent1[p1:p2]
    repair(child1)
    repair(child2)
    return child1, child2


def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        ones = [i for i, b in enumerate(individual) if b == 1]
        zeros = [i for i, b in enumerate(individual) if b == 0]
        if ones and zeros:
            i1 = random.choice(ones)
            i0 = random.choice(zeros)
            individual[i1], individual[i0] = 0, 1
    return individual


def genetic_algorithm(exposures, pop_size=10, generations=20):
    population = create_initial_population(pop_size, len(exposures), 5)

    for gen in range(1, generations+1):
        new_pop = []
        elite = max(population, key=lambda ind: calculate_fitness(ind, exposures))
        new_pop.append(elite)
        while len(new_pop) < pop_size:
            p1 = tournament_selection(population, exposures)
            p2 = tournament_selection(population, exposures)
            while p2 == p1:
                p2 = tournament_selection(population, exposures)

            c1, c2 = crossover(p1, p2)
            new_pop.append(mutate(c1))
            if len(new_pop) < pop_size:
                new_pop.append(mutate(c2))

        population = new_pop

    best = max(population, key=lambda ind: calculate_fitness(ind, exposures))
    return best, calculate_fitness(best, exposures)


def main():
    print("=== GA Solar Panel Placement ===")
    exposures = [8.5, 2.3, 9.1, 4.2, 7.8, 3.1, 6.7, 9.8, 1.5, 5.4]
    print("Exposure list:", exposures)

    best_sol, best_fit = genetic_algorithm(exposures)
    print("\n--- Best Solution ---")
    print("Binary genome:", best_sol)
    print(f"Total exposure: {best_fit:.2f}")


if __name__ == "__main__":
    main()
