import random
import tsplib95 as tsp
import numpy 
import generate 
import instance
import methods
import plot
import os.path

def get_random_permutation(instance):   
    return list(map(lambda x: x + 1, list(numpy.random.permutation(instance.dimension))))

def displaySolution(instance,solution,text):
    print(text,end=': ')
    print(str(instance.calculateGoalFunction(solution)),end=' ')
    if(instance.optimal!=None):
        print("("+str(instance.PRD(instance.calculateGoalFunction(solution)))+"%"+")")
    else:
        print()
    if(instance.format == None):
        plot.draw_plot(instance.instance,solution,text)

def main():
    while(True):
        print("1.Load instance from file")
        menu = int(input("2.Generate random instance\n"))
        if(menu==1):
            name = input("Name: ")
            if(os.path.exists("instances/"+name+".tsp")==True):
                instanc3 = instance.Instance(tsp.read(open("instances/"+name+".tsp")))
            elif(os.path.exists(name+".atsp")==True):
                instanc3 = instance.Instance(tsp.read(open("instances/"+name+".atsp")))
            else:
                print("There is no " + name + " file")
                quit()
        if(menu==2):
            print("1.Euclidean instance")
            print("2.Symetric instance")
            menu = int(input("3.Asymetric instance\n"))
            name = input("Name: ")
            n = int(input("Size: "))
            seed = int(input("Seed: "))
            match menu:
                case 1:
                    generate.EuclideanInstance(name,n,seed)
                case 2:
                    generate.SymetricInstance(name,n,seed)
                case 3:
                    generate.AsymetricInstance(name,n,seed)
            if(os.path.exists("instances/"+name+".tsp")==True):
                instanc3 = instance.Instance(tsp.read(open("instances/"+name+".tsp")))
            elif(os.path.exists("instances/"+name+".atsp")==True):
                instanc3 = instance.Instance(tsp.read("instances/"+open(name+".atsp")))
        
        while(True):
            print("1. k-random")
            print("2. closest neighbour")
            print("3. extended closest neighbour")
            print("4. 2-opt")
            print("5. tabu search")
            print("6. display matrix")
            menu = int(input("7. back\n"))                
            match menu:
                case 1:
                    k = int(input("k: "))
                    k_random = methods.kRandom(k,instanc3)
                    displaySolution(instanc3,k_random,"k-random")
                case 2:
                    closest_neighbour = methods.closestNeighbour(instanc3)
                    displaySolution(instanc3,closest_neighbour,"closest neighbour")
                case 3:
                    extended_closest_neighbour = methods.extendedClosestNeighbour(instanc3)
                    displaySolution(instanc3,extended_closest_neighbour,"extended closest neighbour")
                case 4:
                    opt = methods.OPT(instanc3)
                    displaySolution(instanc3,opt,"2opt")
                case 5:
                    tabu_lenght = int(input("tabu lenght: "))
                    stagnation = int(input("stagnation: "))
                    time = int(input("time: "))
                    tabu = methods.TabuSearch(instanc3,tabu_lenght,stagnation,time)
                    displaySolution(instanc3,tabu,"tabu search")
                case 6:
                    instanc3.displayMatrix()
                case 7:
                    break
main()

