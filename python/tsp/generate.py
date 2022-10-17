import random
import math

def add_line(file, line): 
    f = open(file,"a")
    f.write(line)
    f.close()

def generatePoints(n,seed):
    points = []
    random.seed(seed)
    for i in range(n):
        point = []
        point.append(random.randint(0,999))
        point.append(random.randint(0,999))
        points.append(point)
    return points

def d(x1, y1, x2, y2):
  y = y1 - y2
  x = x1 - x2
  return math.sqrt(y*y+x*x)
        
def generateMatrix(points):
    matrix = [[None for _ in range(len(points))] for _ in range(len(points))]
    for i in range(len(points)):
        for j in range(len(points)):
            matrix[i][j] = round(d(points[i][0],points[i][1],points[j][0],points[j][1]))
    return matrix

def EuclideanInstance(name, n,seed):
    open("instances/"+name+".tsp",'w').close()
    add_line("instances/"+name+".tsp","NAME: "+name+"\n")
    add_line("instances/"+name+".tsp","TYPE: TSP\n")
    add_line("instances/"+name+".tsp","COMMENT: NONE\n")
    add_line("instances/"+name+".tsp","DIMENSION: "+str(n)+"\n")
    add_line("instances/"+name+".tsp","EDGE_WEIGHT_TYPE: EUC_2D\n")
    add_line("instances/"+name+".tsp","NODE_COORD_SECTION\n")
    points = generatePoints(n,seed)
    for i in range(n):
        add_line("instances/"+name+".tsp",str(i+1) + " " + str(points[i][0]) + " " + str(points[i][1]) + "\n")
    add_line("instances/"+name+".tsp","EOF\n")

def SymetricInstance(name, n,seed):
    open("instances/"+name+".tsp",'w').close()
    add_line("instances/"+name+".tsp","NAME: "+name+"\n")
    add_line("instances/"+name+".tsp","TYPE: TSP\n")
    add_line("instances/"+name+".tsp","COMMENT: NONE\n")
    add_line("instances/"+name+".tsp","DIMENSION: "+str(n)+"\n")
    add_line("instances/"+name+".tsp","EDGE_WEIGHT_TYPE: EXPLICIT\n")
    add_line("instances/"+name+".tsp","EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
    add_line("instances/"+name+".tsp","EDGE_WEIGHT_SECTION\n")
    matrix = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i,n):
            if i==j:
                matrix[i][j]=0
            else:
                matrix[i][j]=matrix[j][i]=random.randint(0,999)
    for row in matrix:
        for element in row:
            add_line("instances/"+name+".tsp","{:<3}".format(str(element))+" ")
        add_line("instances/"+name+".tsp","\n")
    add_line("instances/"+name+".tsp","EOF\n")

def AsymetricInstance(name, n,seed):
    open("instances/"+name+".atsp",'w').close()
    add_line("instances/"+name+".atsp","NAME: "+name+"\n")
    add_line("instances/"+name+".atsp","TYPE: ATSP\n")
    add_line("instances/"+name+".atsp","COMMENT: NONE\n")
    add_line("instances/"+name+".atsp","DIMENSION: "+str(n)+"\n")
    add_line("instances/"+name+".atsp","EDGE_WEIGHT_TYPE: EXPLICIT\n")
    add_line("instances/"+name+".atsp","EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
    add_line("instances/"+name+".atsp","EDGE_WEIGHT_SECTION\n")
    random.seed(seed)
    for i in range(n):
        for j in range(n):
            if i==j:
                add_line("instances/"+name+".atsp","{:<3}".format("-1")+" ")
            else:
                add_line("instances/"+name+".atsp","{:<3}".format(str(random.randint(0,999)))+" ")
        add_line("instances/"+name+".atsp","\n")
    add_line("instances/"+name+".atsp","EOF\n")

