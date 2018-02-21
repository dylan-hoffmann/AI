import random as rd
import numpy as np
import math as mt

MAX = 120
NUM_BOX = 10
GENERATIONS = 100
START_POP = 500
#Mutation Chance, I ran a couple loops with the same input with different mutaton rates to try and
#identify the optimal rate, and found it to be around 0.75
XMEN_CHANCE = 0.75


# Boxes are in form [value, weight]
# where 1 <= value <= 20
# and 10 <= weight <= 80
"""
Input: Number of boxes to generate
Output: List of boxes of form: [value, weight]
Function: Generate problem space.
Notes: The value is in the interval [1,20]
and the weight is in the interval [10,80]
"""
def make_boxes(n):
    val_low = 1
    val_high = 20
    w_low = 10
    w_high = 80
    boxes = []
    for x in range(n):
        boxes.append([rd.randint(val_low, val_high), rd.randint(w_low, w_high)])
    return boxes

#Flips a random particle withing the chromosome to introduce variation into the population
"""
Input: 1 Individual (Chromosome)
Output: Alters the individual in place with a randomly selected mutation
Function: Mutate individuals to introduce variation into the population
"""
def mutate(chromo):
    flip = rd.randrange(NUM_BOX)
    chromo[flip] = chromo[flip] ^ 1

#Cross breeding 2 chromosomes
#Pick a random point, and combine into a new individual
"""
Input: 2 parents (Chromosomes), population list
Output: Appends the child to the end of the population list
Function: Crossbreed fitter individuals in order to avoid local extrema
"""
def cross(chromo1, chromo2, pop):
    Xpoint = rd.randrange(NUM_BOX)
    p1 = chromo1[Xpoint:]
    p2 = chromo2[Xpoint:]
    child1 = chromo1[:Xpoint]
    child1.extend(p2)
    pop.append([0, child1])

"""
Fitness Function
Input: 1 individual, list of boxes
Output: Value of the boxes contained within this individual
Function: Calculate the fitness of an individual based on the value of the boxes.
If the weight goes over the maximum, return the negative of the weight. More overweight individuals are deemed
less fit than less overweight individuals 
"""
def fitness(chromo, boxes):
    weight = 0
    value = 0
    for i in range(NUM_BOX):
        if chromo[i] == 1:
            value += boxes[i][0]
            weight += boxes[i][1]
    if weight > MAX:
        value = weight * -1
    return value


"""
Mutate Chance Function
Input: 1 individual, current fittest individual, list of boxes
Output: Chance of mutating the child
Function: Calculate the chance of mutting a child based on the inverse of its fitness
Essentially this allows thos program to combine the approaches of Genetic Algorithms and simulated annealing
By weighing the tolerance for changing a gene against its fitness. I considered including generation as well, so there
was a greater mutation chance earlier on, but didn't have a chance to test how it would impact my results
"""
def mutate_chance(child, fittest, boxes):
    fit = fitness(child, boxes)
    if fit > 0:
        chance = XMEN_CHANCE * (float(fittest)/float(fit))
    else:
        chance = 0
    return chance


# Pop is a list where element is in the form:
# [fitness, Chromosome]
"""
Abiogenesis Function
Input: Population list (Empty)
Output: The starting population
Function: Generate the stating population. There is a 70% chance of mot including a box, and a 30% chance of including
a box.
Each chomosome is a bit list of the length of the number of boxes, were a 1 corresponds to including the box, and a zero
corresponds to not.
"""
def abiogenesis(pop):
    for i in range(START_POP):
        pop.append([0, np.ndarray.tolist(np.random.choice([0, 1], size=(NUM_BOX,), p=[0.7, 0.3]))])


# 1 Generation is as follows:
#   Apply fitness function to all chromosomes
#   Sort Population
#   Cull bottom 50%
#   Crossbreed population
#   Mutate n random individuals, where n is a random # between 0 and pop size/2
#   Repeat
"""
Evolve Function
Input: Population list, boxes list
Output: The fittest solution found in the specified number of generations
Function: Iteratively determine the fittest individual where the process for one generation is as follows:
    Apply fitness function to all chromosomes
    Sort Population
    Cull bottom 50%
    Crossbreed population
    Random chance of mutating the child by a factor weighted by its fitness
    Repeat
"""
def evolve(popul, boxes):
    gen = 0
    while gen < GENERATIONS:
        cull = int(mt.ceil(len(popul) / 2))
        x = popul[:cull]
        popul = x
        leng = len(popul)
        fittest = max(popul)[0]
        for i in range(leng):
            #Select 2 individuals to cross breed. Random selection, but weighted towards more fit individuals
            p1 = int(mt.floor(len(popul) * (rd.random() ** 2)))
            p2 = int(mt.floor(len(popul) * (rd.random() ** 2)))
            cross(popul[p1][1], popul[p2][1], popul)
            if rd.random() > mutate_chance(popul[-1][1], fittest, boxes):
                mutate(popul[-1][1])
        gen += 1
        for ind in popul:
            ind[0] = fitness(ind[1], boxes)
        popul.sort(reverse=True)

    return max(popul)



def main():
    result = []
    for iter in range(1):
        #global XMEN_CHANCE
        #XMEN_CHANCE = float(iter) / 100.0
        val = 0
        for test in range(1000):
            boxes = make_boxes(NUM_BOX)
            pop = []
            abiogenesis(pop)
            for i in pop:
                i[0] = fitness(i[1], boxes)
            pop.sort(reverse=True)


            best = evolve(pop, boxes)
            weight = 0
            for i in range(NUM_BOX):
                if best[1][i] == 1:
                    weight += boxes[i][1]
            if best[0] < 0:
                print weight, best
                print boxes
                print ""

            val += best[0]
        result.append([XMEN_CHANCE, val/50])
    for i in result:
        print(i)

if "__main__" == __name__:
    main()


