import numpy 
import random
import instance 
import time

def get_random_permutation(instance):   
    return list(map(lambda x: x + 1, list(numpy.random.permutation(instance.dimension))))

def invert(permutation,i,j):
    p = 1
    copy2 = permutation.copy()
    copy = permutation.copy()
    for k in range(i-1,j):
        copy2[k]=copy[j-p]
        p+=1
    return copy2

def swap(permutation,i,j):
    copy = permutation.copy()
    temp = copy[i-1]
    copy[i-1] = copy[j-1]
    copy[j-1] = temp
    return copy

def kRandom(k, instance):
    minimum = 10000000
    minimum_permutation = []
    for i in range(k):
        permutation = get_random_permutation(instance.instance)
        goal_function = instance.calculateGoalFunction(permutation)
        if(goal_function<minimum):
            minimum = goal_function
            minimum_permutation = permutation
    return minimum_permutation

def closestNeighbour(instance):
    matrix = instance.matrix
    result = []
    been = []
    node = random.randint(0,instance.dimension-1)
    result.append(node)
    minimum_index = 0
    been.append(node)
    for j in range(instance.dimension-1):
        minimum_value = 10000000
        for i in range(instance.dimension):
            if(been.count(i)==0 and matrix[node][i]<minimum_value and i != node):
                minimum_value = matrix[node][i]
                minimum_index=i
        been.append(minimum_index)
        result.append(minimum_index)
        node = minimum_index
    for x in range(len(result)):
       result[x] = result[x]+1
    return result

def extendedClosestNeighbour(instance):
    minimum_lenght = 10000000
    matrix = instance.matrix
    minimum_solution=[]
    for k in range(instance.dimension):
        result = []
        been = []
        node = k
        result.append(node)
        minimum_index = 0
        been.append(node)
        for j in range(instance.dimension-1):
            minimum_value = 10000000
            for i in range(instance.dimension):
                if(been.count(i)==0 and matrix[node][i]<minimum_value and i != node):
                    minimum_value = matrix[node][i]
                    minimum_index=i
            been.append(minimum_index)
            result.append(minimum_index)
            node = minimum_index
        for x in range(len(result)):
            result[x] = result[x]+1
        if(instance.calculateGoalFunction(result)<minimum_lenght):
            minimum_lenght=instance.calculateGoalFunction(result)
            minimum_solution = result
    return minimum_solution

def OPT(instance):
    permutation = get_random_permutation(instance)
    change = True
    minimum_permutation = []
    while(change==True):
        minimum_lenght = 10000000
        for i in range(1,instance.dimension+1):
            for j in range(i,instance.dimension+1):
                actual = invert(permutation,i,j)
                if(instance.calculateGoalFunction(actual)<minimum_lenght):
                    minimum_lenght = instance.calculateGoalFunction(actual)
                    minimum_permutation = actual
        if(minimum_permutation==permutation):
            change = False
        permutation = minimum_permutation
    return permutation

def TabuSearch(instance,tabu_lenght,stagnation,t):
    tabu = []
    memory = []
    permutation = get_random_permutation(instance)
    best = permutation
    worse = 0
    minimum_permutation = []
    was_added = False
    t_end = time.time() + t
    while time.time() < t_end: 
        minimum_lenght = 10000000
        for i in range(1,instance.dimension+1):
            for j in range(i+1,instance.dimension+1):
                if (i,j) not in tabu:   # add cryterium of aspiration??
                    actual = invert(permutation,i,j)
                    if(instance.calculateGoalFunction(actual)<minimum_lenght):
                        minimum_lenght = instance.calculateGoalFunction(actual)
                        minimum_permutation = actual
                        minimum_ij = (i,j)
        tabu.append(minimum_ij)
        if was_added == True:
            memory[-1][1].append(minimum_ij)
            was_added = False
        if(len(tabu)>tabu_lenght):
            tabu.pop(0)
        if minimum_lenght >= instance.calculateGoalFunction(permutation):
            worse += 1
        else:
            worse = 0
            if minimum_lenght < instance.calculateGoalFunction(best):
                best = minimum_permutation
                memory.append((best,tabu))
                was_added = True
        permutation = minimum_permutation
        if worse == stagnation:
            permutation = memory[-1][0]
            tabu = memory[-1][1]
            memory.pop(0)
    return best
