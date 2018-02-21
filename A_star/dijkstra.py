import random as rd
import heapq as hq

num_pancakes = 5
frontier = []
visited = []
goal = [0,1,2,3,4,5]


# node = [least cost seen, pancake order (list of #s), parent)

def cook_pancakes(pancakes):
    pancakes = range(1, num_pancakes + 1)
    plate = [0]
    rd.shuffle(pancakes)
    pancakes = plate + pancakes
    return pancakes



# returns the best option
def f(x):
    return hq.heappop(frontier)


# cost function, backwards cost is handled inline
def g(x):
    return num_pancakes - x


def flip(curr_stack, k):
    flip_stack = curr_stack[k:]
    curr_stack = curr_stack[:k]
    flip_stack.reverse()
    curr_stack = curr_stack + flip_stack
    return curr_stack


def expand(x):
    for i in range(1, num_pancakes):
        child_stack = flip(x[1], i)
        cost = g(i) + x[0]
        contan = contains(frontier, child_stack)
        if contan == -1 and (child_stack not in visited):
            hq.heappush(frontier, [cost, child_stack, x])
        elif contan > -1:
            if frontier[contan][0] > cost:
                frontier[contan][0] = cost
                frontier[contan][2] = x


def search(start):
    hq.heappush(frontier, [0, start, []])
    i = 0
    while (frontier):
        print i
        i +=1
        currnode = hq.heappop(frontier)
        visited.append(currnode[1])
        if (currnode[1] == goal):
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
        if node_list[i][1] == match:
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