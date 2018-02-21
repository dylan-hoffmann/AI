import random as rd
import numpy as np
import math as mt

MAX = 120
NUM_BOX = 30
GENERATIONS = 100
START_POP = 500
XMEN_CHANCE = 0.75


# Boxes are in form [value, weight]
# where 1 <= value <= 20
# and 20 <= weight <= 200
def make_boxes(n):
    val_low = 1
    val_high = 20
    w_low = 10
    w_high = 80
    boxes = []
    for x in range(n):
        boxes.append([rd.randint(val_low, val_high), rd.randint(w_low, w_high)])
    return boxes


def mutate(chromo):
    flip = rd.randrange(NUM_BOX)
    chromo[flip] = chromo[flip] ^ 1


def cross(chromo1, chromo2, pop):
    Xpoint = rd.randrange(NUM_BOX)
    p1 = chromo1[Xpoint:]
    p2 = chromo2[Xpoint:]
    child1 = chromo1[:Xpoint]
    child2 = chromo2[:Xpoint]
    child1.extend(p2)
#    child2.extend(p1)
    pop.append([0, child1])
 #   pop.append([0, child2])


def fitness(chromo, boxes):
    weight = 0
    value = 0
    for i in range(NUM_BOX):
        if chromo[i] == 1:
            value += boxes[i][0]
            weight += boxes[i][1]
            if weight > MAX:
                # print weight
                return -1*weight
    return value


# Pop is a list where element is in the form:
# [fitness, Chromosome]
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
def evolve(popul, boxes):
    gen = 0
    while gen < GENERATIONS:
        #        for i in pop:
        #            print i
        cull = int(mt.ceil(len(popul) / 2))
        # print "cull",cull
        x = popul[:cull]
        popul = x
        leng = len(popul)
        for i in range(leng):
            p1 = int(mt.floor(len(popul) * (rd.random() ** 2)))
            p2 = int(mt.floor(len(popul) * (rd.random() ** 2)))
            cross(popul[p1][1], popul[p2][1], popul)
            if rd.random() < XMEN_CHANCE:
                mutate(popul[-1][1])
        """
        mut = rd.randrange(len(pop))
        for i in range(mut):
            mutate(pop[rd.randrange(len(pop))][1])
        """
        gen += 1
        for ind in popul:
            ind[0] = fitness(ind[1], boxes)
        popul.sort(reverse=True)

    return max(popul)



def main():
    result = []
    for iter in range(72,78):
        #global XMEN_CHANCE
        #XMEN_CHANCE = float(iter) / 100.0
        val = 0
        for test in range(1000):
            boxes = make_boxes(NUM_BOX)
            #boxes = [[14, 36], [6, 31], [11, 44], [4, 30], [5, 54], [6, 41], [14, 17], [18, 43], [19, 71], [14, 67], [7, 65], [1, 46], [13, 18], [5, 11], [3, 60], [10, 43], [16, 29], [9, 61], [2, 80], [10, 32], [13, 40], [15, 36], [14, 56], [19, 65], [11, 16], [1, 40], [6, 60], [2, 68], [10, 32], [6, 78]]
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


