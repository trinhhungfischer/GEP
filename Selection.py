"""
||========================================================||
|| This is my label for every program which coded by Hung ||
||========================================================||
"""

from Encode_Evaluate import RMSE, valid_chromosome
from Initialization import init_population
from random import random

# Some constants in this program
population = init_population(50)
NP = 50

# First we will evaluate of fitness function of all individual in
# this generation which will store in list
def fitness(population = []):
    fitness = []
    i = 0
    while i < len(population):
        try:
            fitness.append(RMSE(population[i]))
            i += 1
        except Exception as error:
            population.pop(i)
    return fitness

def one_minus_similarity(chrome1 = '', chrome2 = ''):
    s1, l1 = valid_chromosome(chrome1)
    s2, l2 = valid_chromosome(chrome2)
    overlap = sum(1 for i in range(min(l1, l2)) if s1[i] == s2[i])
    return 1 - 2.0 * overlap / (l1 + l2)

def q_roulette_wheel(population = []):
    fit = fitness(population)
    best = fit[0]
    i_best = 0
    for i in range(len(fit)):
        if fit[i] < best:
            best = fit[i]
            i_best = i

    p = []
    s = 0
    for i in range(len(fit)): # Make iteration of roulette wheel is NP
        pi = one_minus_similarity(population[i_best], population[i])
        s += pi
        p.append(pi)
    for i in range(len(fit)):
        p[i] /= s

    q = []
    for i in range(len(fit)): # Make iteration of roulette wheel is NP
        q.append(sum(p[:i+1]))
    return q

def roulette_wheel_selection(population = []):
    q_list = q_roulette_wheel(population)
    l = len(q_list)
    new = []

    it = 0
    while it < NP:
        r = random()
        for i in range(l):
            if q_list[i] > r:
                break
        new.append(population[i-1])
        it += 1

    return new

def rank_selection(population = []):
    Y = fitness(population)
    Z = [x for _, x in sorted(zip(Y, population))]
    if len(Z) <= 50:
        K = Z
        return Z
    else:
        K = Z[:50]
        return Z[:50]

# This function decide kind of select to choose
def selection(population = []):
    return roulette_wheel_selection(population)

if __name__ == '__main__':
    pass