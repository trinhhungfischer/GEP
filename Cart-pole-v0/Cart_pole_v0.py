"""
||========================================================||
|| This is my label for every program which coded by Hung ||
||========================================================||
"""

import gym
import random
import matplotlib.pyplot as plt
from statistics import mean

env = gym.make("CartPole-v0")
env.reset()

# Some constant in this program
NUM_GENS = 1000
TIMESTEP_LIMIT = 1000


class GeneticOperator:

    def __init__(self, pm=.1, pc=.1, pc1=.4, pc2=.7, pis=.4, pris=.4, pi=.1):
        self.pm = pm
        self.pi = pi
        self.pc = pc
        self.pc1 = pc1
        self.pc2 = pc2
        self.pis = pis
        self.pris = pris

    def mutation(self, population=[]):
        NP = len(population)
        for i in range(NP):
            mutated = list(population[i])
            # Mutated each chromosome in population
            for j in range(len(mutated)):
                r = random.random()
                if r < self.pm:
                    mutated[j] = random.choice(['0', '1'])
            population.append(''.join(mutated))
        return population

    def inversion(self, population=[]):
        NP = len(population)
        for i in range(NP):
            if random.random() < self.pi:
                position = random.choices(range(len(population[i])), k=2)
                crack1, crack2 = min(position), max(position)
                new_gene = population[i][:crack1] + population[i][crack2:crack1:-1] \
                           + population[i][crack2:]

                population.append(new_gene)

        return population

    def is_transportation(self, population=[]):
        NP = len(population)
        for i in range(NP):
            if random.random() < self.pis:
                j = random.choice(range(NP))

                # i-th individual is the trans gene which received IS
                # j-th individual is the ori gene which cut its IS
                position = random.choices(range(len(population[j])), k=2)
                crack1, crack2 = min(position), max(position)
                k = crack2 - crack1
                # Find pos trans in the receive gene to insert
                pos_trans = random.randint(1, len(population[i]) - k)

                new_gene = population[i][0:pos_trans] + population[j][crack1:crack2] + \
                           population[i][pos_trans + k:]

                population.append(new_gene)

        return population

    def ris_transportation(self, population=[]):
        NP = len(population)

        for i in range(NP):
            if random.random() < self.pris:
                j = random.choice(range(NP))

                # i-th individual is the trans gene which received IS
                # j-th individual is the ori gene which cut its IS
                crack1, k = random.choices(range(int(len(population[j]) / 2)), k=2)
                crack1 = random.choice(range(int(len(population[j]) / 2)))

                new_gene = population[j][crack1:crack1 + k] + population[i][k:]
                population.append(new_gene)

        return population

    def crossover_1point(self, population=[]):
        NP = len(population)

        for i in range(int(NP / 2)):
            cr1 = random.random()
            if cr1 < self.pc:
                chrome1, chrome2 = random.choices(population, k=2)
                crack = random.randint(0, len(chrome1))
                c1_new = chrome1[:crack] + chrome2[crack:]
                c2_new = chrome2[:crack] + chrome1[crack:]
                population.append(c1_new)
                population.append(c2_new)

        return population

    def crossover(self, population=[], best=''):
        NP = len(population)

        for i in range(int(NP / 2)):
            cr1 = random.random()
            if cr1 < self.pc1:
                chrome1 = best
                chrome2 = random.choice(population)
                crack = random.randint(0, len(chrome1))
                c1_new = chrome1[:crack] + chrome2[crack:]
                c2_new = chrome2[:crack] + chrome1[crack:]
                population.append(c1_new)
                population.append(c2_new)

        return population

    def crossover_2point(self, population=[]):
        NP = len(population)

        for i in range(int(NP / 2)):
            cr2 = random.random()
            if cr2 < self.pc2:
                chrome1, chrome2 = random.choices(population, k=2)
                position = random.choices(range(len(chrome1)), k=2)
                crack1, crack2 = min(position), max(position)
                c1_new = chrome1[:crack1] + chrome2[crack1:crack2] + chrome1[crack2:]
                c2_new = chrome2[:crack1] + chrome1[crack1:crack2] + chrome2[crack2:]
                population.append(c1_new)
                population.append(c2_new)

        return population


def pause(population=[]):
    list = fitness(population)
    for i in range(len(population)):
        if (list[i] == 1500):
            return True, i, '', 0

    max1 = max(list)
    i_max = list.index(max1)

    return False, max1, population[i_max], mean(list)


def init_population(NP=50):
    pop = []
    for i in range(NP):
        ind = ''
        for j in range(TIMESTEP_LIMIT):
            ind += random.choice(['0', '1'])
        pop.append(ind)
    return pop


def evaluate_fitness(ind=''):
    observation = env.reset()
    score = 0
    env.seed(0)
    for t in range(TIMESTEP_LIMIT):
        observation, reward, done, info = env.step(int(ind[t]))
        if done:
            break
        score += reward
    return score


# First we will evaluate of fitness function of all individual in
# this generation which will store in list
def fitness(population=[]):
    fitness = []
    for i in range(len(population)):
        fitness.append(evaluate_fitness(population[i]))
    return fitness


def roulette_selection(population=[], num=50):
    fit_list = fitness(population)
    s = sum(fit_list)
    l = len(fit_list)

    # probability chosen of individual
    p_chosen = list(ind / s for ind in fit_list)
    q_list = []
    for i in range(len(population)):
        q_list.append(sum(p_chosen[:i]))

    new = []  # This list is to store new generations
    it = 0  # Number of iteration of roulette wheel
    while it < num:
        r = random.random()
        for id in range(l):
            if q_list[id] > r:
                break

        new.append(population[id - 1])
        it += 1

    return new


def rank_selection(population=[], NP=50):
    Y = fitness(population)
    zip_list = zip(Y, population)
    sorted_pairs = sorted(zip_list, reverse=True)

    tuples = zip(*sorted_pairs)
    Y, Z = [list(tuple) for tuple in tuples]
    return Z[:NP]


"""
This function is main of this program to demonstrate Genetic
Expression Programming in real life
"""

# Statistic
def GA_model():
    GA = GeneticOperator(0.5, 0.01)
    population = init_population(500)
    gen = 1
    fitness_history_max = []
    fitness_history_mean = []
    while (gen <= NUM_GENS):
        parent = rank_selection(population, 100)
        done, fit_max, best, fit_mean = pause(population)
        if done:
            break
        fitness_history_max.append(fit_max)
        fitness_history_mean.append(fit_mean)
        print('This is gen {} has best ind {} has mean {}'.format(gen, fit_max, fit_mean))
        # env.reset()
        # for t in range(TIMESTEP_LIMIT):
        #     observation, reward, done, info = env.step(int(best[t]))
        #     env.render()
        #     if done:
        #         break
        mutant = GA.mutation(parent)
        off_string = GA.crossover_1point(mutant)
        population = off_string
        gen += 1

    return fitness_history_max, fitness_history_mean


if __name__ == '__main__':
    fitness_history_max, fitness_history_mean = GA_model()

    plt.plot(list(range(NUM_GENS)), fitness_history_mean, label='Mean Fitness')
    plt.plot(list(range(NUM_GENS)), fitness_history_max, label='Max Fitness')
    plt.legend()
    plt.title('Fitness through the generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()
