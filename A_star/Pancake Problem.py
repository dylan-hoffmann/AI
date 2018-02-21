import random as rd
import heapq as hq

num_pancakes = 5
frontier = []
visited = []

#node = [least cost seen, pancake order (list of #s), parent)

def cook_pancakes(pancakes):
    pancakes = range(1,num_pancakes+1)
    plate = [0]
    rd.shuffle(pancakes)
    pancakes = plate + pancakes
    return pancakes

#Heuristic function
def h(x):
    dist = 0
    num = num_pancakes
    if num_pancakes % 2 == 1:
        num = num - 1
    for i in range(1,num, 2):
        if (abs(x[i-1] - x[i]) != 1):
            dist += 1
        if (abs(x[i+1] - x[i]) != 1):
            dist += 1
    return dist


# returns the best option
def f(x):
    return hq.heappop(frontier)

#cost function, backwards cost is handled inline
def g(x):
    return num_pancakes-x


def flip(curr_stack, k):
    flip_stack = curr_stack[k:]
    curr_stack = curr_stack[:k]
    flip_stack.reverse()
    curr_stack = curr_stack + flip_stack
    return curr_stack


def expand(x):
    for i in range(1,num_pancakes):
        child_stack = flip(x[1], i)
        cost = g(i) + x[0] + h(child_stack)
        contan = contains(frontier, child_stack)
        if contan > -1:
            if frontier[contan][0] > cost:
                frontier[contan][0] = cost
                frontier[contan][2] = x
        else:
            if child_stack not in visited:
                hq.heappush(frontier, [cost,child_stack,x])


def search(start):
    hq.heappush(frontier,[0,start, []])
    i = 0
    while(frontier):
        print i
        i += 1
        currnode = hq.heappop(frontier)
        visited.append(currnode[1])
        if h(currnode[1]) == 0:
            path = trace(currnode)
            return path
        expand(currnode)


    return []


def trace(node):
    path = []
    while (node[2]):
        path.append(node[1])
        node = node[2]
    path.reverse()
    return path


def contains(node_list, match):
    for i in range(len(node_list)):
        if node_list[i][1] ==  match:
            return i
    return -1


def main():

    pancakes = []
    path = []
    pancakes = cook_pancakes(pancakes)
    print(pancakes)
    print("")
    path = search(pancakes)
    for i in range(len(path)):
        print(path[i])
    """
    for i in range(20):
        pancakes = cook_pancakes(pancakes)
        print pancakes
        print(h(pancakes))
        
    """




if __name__ == "__main__":
    main()