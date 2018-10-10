import argparse
import collections
import random
import math
import statistics
from pprint import pprint

Instance = collections.namedtuple('Instance', ['n', 'values', 'probabilities'])

class Algorithm(object):
    def __init__(self, config):
        self.config = config
        self.read_instance()
        random.seed(self.config.seed)

    def read_instance(self):
        with open(self.config.instance_file) as file:
            n = int(file.readline())

            values = []
            for i in range(n):
                values.append(float(file.readline()))

            probabilites = []
            for i in range(n):
                probabilites.append([])
                for j in range(n):
                    probabilites[i].append(float(file.readline()))

        self.instance = Instance(n, values, probabilites)

    # @profile
    def expected_damage(self, assignment):
        total = 0.0
        used_weapons = set()
        probabilities = self.instance.probabilities
        values = self.instance.values
        for i in range(self.instance.n):
            j = assignment[i]

            if j in used_weapons:
                continue

            used_weapons.add(j)
            total += probabilities[i][j]*values[i]

        return total

    # @profile
    def fitness(self, assignment):
        total = sum(self.instance.values)
        damage = self.expected_damage(assignment)
        return -(total - damage)

    # @profile
    def generate_initial_population(self):
        population = []
        weapons = list(range(self.instance.n))
        for i in range(self.config.population_size):
            assignment = [random.choice(weapons) for _ in range(self.instance.n)]
            population.append(assignment)

        return population

    # @profile
    def select_best_individuals(self, population):
        tournament_size = int(math.ceil(self.config.tournament_size*len(population)))

        selected = []
        while len(selected) < self.config.selection_size*len(population):
            competitors = random.sample(population, tournament_size)
            competitors.sort(key=lambda a: self.fitness(a), reverse=True)
            for competitor in competitors:
                if random.random() < self.config.selection_probability:
                    selected.append(list(competitor))
                    break

        return selected

    # @profile
    def crossover(self, individuals):
        population = []

        for i in range(self.config.population_size):
            father, mother = random.sample(individuals, 2)
            point = random.randint(0, self.instance.n-1)
            child = father[:point] + mother[point:]
            population.append(child)

        return population

    # @profile
    def mutate(self, population):
        population = list(population)

        for i, individual in enumerate(population):
            if random.random() > self.config.mutation_probability:
                continue

            mutated_individual = list(individual)
            if self.config.mutation_method == 'random':
                point = random.randint(0, self.instance.n-1)
                mutated_individual[point] = random.randint(0, self.instance.n-1)
            elif self.config.mutation_method == 'swap':
                a = random.randint(0, self.instance.n-1)
                b = random.randint(0, self.instance.n-1)
                mutated_individual[a], mutated_individual[b] = mutated_individual[b], mutated_individual[a]

            population[i] = mutated_individual

        return population

    # @profile
    def report(self, iteration, population):
        fitnesses = [self.fitness(a) for a in population]
        return 'gen: {}, avg: {}, std: {}, max: {}, min: {}'.format(
            iteration,
            statistics.mean(fitnesses),
            statistics.stdev(fitnesses),
            max(fitnesses),
            min(fitnesses),
        )

    def write_results(self, reports, population):
        parameters = []
        for k, v in vars(self.config).iteritems():
            if k == 'instance_file':
                v = v.replace('/', '_')
            parameters.append('{}={}'.format(k, v))

        with open('results/'+ '-'.join(parameters)+'.txt', 'w') as file:
            final_population = sorted([(self.fitness(a), a) for a in population], reverse=True)
            file.write(str(final_population[0][0]))
            file.write('\n\n')

            file.write('\n'.join(parameters))
            file.write('\n\n')

            file.write('\n'.join(reports))
            file.write('\n\n')

            file.write('\n'.join([str(p) for p in final_population]))
            file.write('\n')

    # @profile
    def run(self):
        population = self.generate_initial_population()
        iteration = 0
        reports = []
        while iteration < self.config.max_iterations:
            report = self.report(iteration, population)
            reports.append(report)
            print report
            for i in range(self.config.max_iterations/10): # TODO: config.num_reports
                best_individuals = self.select_best_individuals(population) # TODO: config.selection_criteria
                population = self.crossover(best_individuals)
                population = self.mutate(population)
                iteration += 1

        report = self.report(iteration, population)
        reports.append(report)
        print report
        self.write_results(reports, population)
        # pprint(sorted([(a, self.fitness(a)) for a in population], key=lambda p: p[1], reverse=True)[0])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--instance-file',
        help='File containing the problem instance',
        required=True,
    )
    parser.add_argument(
        '--population-size',
        help='The number of individuals in the population',
        type=int,
        required=True,
    )
    parser.add_argument(
        '--max-iterations',
        help='The maximum numbers of generations the algorithm will evaluate',
        type=int,
        required=True,
    )
    parser.add_argument(
        '--tournament-size',
        help='The number of individuals in a tournament expressed as a fraction of the population size',
        type=float,
        required=True,
    )
    parser.add_argument(
        '--selection-probability',
        help='The selection probability for the tournament rounds',
        type=float,
        required=True,
    )
    parser.add_argument(
        '--selection-size',
        help='The number of individuals selected for the next generation expressed as a fraction of the population size',
        type=float,
        required=True,
    )
    parser.add_argument(
        '--mutation-probability',
        help='The probability an individual will mutate in the mutation step',
        type=float,
        required=True,
    )
    parser.add_argument(
        '--mutation-method',
        help='How to perform the mutation (swap or random)',
        required=True,
    )
    parser.add_argument(
        '--seed',
        help='Seed for the random number generator',
        type=int,
        required=True,
    )
    args = parser.parse_args()
    Algorithm(args).run()

if __name__ == '__main__':
    main()
