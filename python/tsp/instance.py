import math
import os.path
import tsplib95 as tsp
import methods

def d(x1, y1, x2, y2):
    y = y1 - y2
    x = x1 - x2
    return math.sqrt(y*y+x*x)

class Instance:
    def __init__(self, instance):
        self.instance = instance
        self.name = "instances/"+instance.name
        self.type = instance.type
        self.dimension = int(instance.dimension)
        self.format = instance.edge_weight_format
        self.matrix = self.getMatrix()
        if(os.path.exists(self.name+".opt.tour")==True):
            self.optimal = self.calculateGoalFunction(tsp.read(open(self.name+".opt.tour")).tours[0])
        else:
            self.optimal = None

    def getMatrix(self):
        if self.type=="TSP":
            match self.format:
                case "LOWER_DIAG_ROW":  
                    row_size = 1
                    matrix = []
                    matrix2 = []
                    row=[]
                    for i in range(len(self.instance.edge_weights)):
                        for j in range(len(self.instance.edge_weights[i])):
                            row.append(self.instance.edge_weights[i][j])
                            if len(row)==row_size:
                                matrix.append(row)
                                row=[]
                                row_size = row_size + 1
                    row = []
                    for j in range(len(matrix)):
                        for i in range(len(matrix)):
                            if(len(matrix[i])>j+1):
                                row.append(matrix[i][j])
                        matrix2.append(row)
                        row = []
                    for x in matrix2:
                        x.insert(0,0)
                    for i in range(len(matrix2)):
                        for j in range(i):
                            matrix2[i].insert(0,matrix2[i-j-1][i])
                    return matrix2
                case "FULL_MATRIX":
                    return self.instance.edge_weights
                case None:
                    matrix = [[None for _ in range(len(self.instance.node_coords))] for _ in range(len(self.instance.node_coords))]
                    for i in range(len(self.instance.node_coords)):
                        for j in range(len(self.instance.node_coords)):
                            matrix[i][j]=round(d(self.instance.node_coords[i+1][0],self.instance.node_coords[i+1][1],self.instance.node_coords[j+1][0],self.instance.node_coords[j+1][1]))
                    return matrix
        elif self.type=="ATSP":
            matrix = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
            distances = []
            for row in self.instance.edge_weights:
                for distance in row:
                    distances.append(distance)
            for i in range(self.dimension):
                for j in range(self.dimension):
                    matrix[i][j] = distances[i*self.instance.dimension+j]
            return matrix

    def calculateGoalFunction(self,solution):
        result = 0
        solution.append(solution[0])
        for i in range(len(solution)-1):
            result += self.matrix[solution[i]-1][solution[i+1]-1]
        solution.pop()
        return result

    def PRD(self, x):
        x_ref = self.optimal
        return round((x-x_ref)/x_ref*100)
    
    def displayMatrix(self):
        for row in self.matrix:
            for element in row:
                print("{:<4}".format(str(element)),end=' ')
            print()
        print()

        