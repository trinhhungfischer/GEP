"""
||========================================================||
|| This is my label for every program which coded by Hung ||
||========================================================||
"""

# Python program to create random chromosome

import random

# Function node set is {+,-,*,/,sqrt(Q),exp(E),sin(s)}
# Terminal node set is {x, y}
head_set = list('+-*/QEsx')
ter_set = ['x']

# Make a seed to reuse a random population
random.seed(7)

# Traditional method to randomly assign to each element of chromosome
# Depend on its position in chromosome (head, tail)
def init_one(h = 10):
    str = []
    for i in range (h):
        ele = random.choice(head_set)
        str.append(ele)
    for i in range (h + 1):
        ele = random.choice(ter_set)
        str.append(ele)
    return ''.join(str)

def init_population(NP = 50, h = 10):
    pop = []
    for i in range (NP):
        pop.append(init_one(h))
    return pop
