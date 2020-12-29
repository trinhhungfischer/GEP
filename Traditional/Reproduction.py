"""
||========================================================||
|| This is my label for every program which coded by Hung ||
||========================================================||
"""


# Python program to build and evaluate expression tree
# Function node set is {+,-,*,/,sqrt(Q),exp(E),sin(s)}
# Terminal node set is {x, y, ?}

from random import random, choice, choices, randint, getstate
from Initialization import init_population
from Selection import selection

# Some constants in this program
population = init_population()
head_set = list('+-*/QEsx')
func_set = list('+-*/QEs')
ter_set = ['x']
h = 10

def mutation(population = [], pm = .1):
    NP = len(population)

    for i in range(NP):
        mutated = list(population[i])
        # Mutated each chromosome in population
        for i in range(len(mutated)):
            r = random()
            if r < pm:
                if i < h:
                    mutated[i] = choice(head_set)
                else:
                    mutated[i] = choice(ter_set)
        population[i] = ''.join(mutated)
    return population

def inversion(population = [], pi = .1):
    NP = len(population)

    for i in range (NP):
        if random() < pi:
            position = choices(range(len(population[i])), k=2)
            crack1, crack2 = min(position), max(position)
            new_gene = population[i][:crack1] + population[i][crack2:crack1:-1]\
                       + population[i][crack2:]
            
            population[i] = new_gene
            
    return population

# Transportation step of evolution operators
def is_transportation(population = [], pis = .1):
    NP = len(population)

    for i in range(NP):
        if random() < pis:
            j = choice(range(NP))

            # i-th individual is the trans gene which received IS
            # j-th individual is the ori gene which cut its IS
            position = choices(range(len(population[j])), k=2)
            crack1, crack2 = min(position), max(position)
            k = crack2 - crack1
            # Find pos trans in the receive gene to insert
            pos_trans = randint(1, len(population[i]) - k)

            new_gene = population[i][0:pos_trans] + population[j][crack1:crack2] + \
                population[i][pos_trans + k:]

            population[i] = new_gene

    return population

def ris_transportation(population = [], pris = .1):
    NP = len(population)

    for i in range(NP):
        if random() < pris:
            j = choice(range(NP))

            # i-th individual is the trans gene which received IS
            # j-th individual is the ori gene which cut its IS
            crack1, k = choices(range(int(len(population[j]) / 2)), k=2)

            while ter_set.count(population[j][crack1]):
                crack1 = choice(range(int(len(population[j]) / 2)))
            new_gene = population[j][crack1:crack1+k] + population[i][k:]
            population[i] = new_gene

    return population

# Recombination step of evolution operators
def crossover_1point(population = [], pc1 = .7):
    NP = len(population)

    for i in range(int(NP/2)):
        cr1 = random()
        if cr1 < pc1:
            chrome1, chrome2 = choices(population, k=2)
            crack = randint(0, len(chrome1))
            c1_new = chrome1[:crack] + chrome2[crack:]
            c2_new = chrome2[:crack] + chrome1[crack:]
            population.append(c1_new)
            population.append(c2_new)

    return population

def crossover_2point(population = [], pc2 = .7):
    NP = len(population)

    for i in range(int(NP / 2)):
        cr2 = random()
        if cr2 < pc2:
            chrome1, chrome2 = choices(population, k=2)
            position = choices(range(len(chrome1)), k=2)
            crack1, crack2 = min(position), max(position)
            c1_new = chrome1[:crack1] + chrome2[crack1:crack2] + chrome1[crack2:]
            c2_new = chrome2[:crack1] + chrome1[crack1:crack2] + chrome2[crack2:]
            population.append(c1_new)
            population.append(c2_new)

    return population

def reproduction(population=[], pm=.1, pc1=.7, pc2=.7, \
                 pis=.1, pris=.1, pi=.1):
    next_mutated = mutation(population, pm)
    next_inversed = inversion(next_mutated, pi)
    next_is_trans = is_transportation(next_inversed, pis)
    next_ris_trans = ris_transportation(next_is_trans, pris)
    next_cr1 = crossover_1point(next_ris_trans, pc1)
    next_cr2 = crossover_2point(next_cr1, pc2)
    next = selection(next_cr2)
    return next

if __name__ == '__main__':
    population = init_population()
    print(population)
    print(inversion(population))