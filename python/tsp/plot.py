import matplotlib.pyplot as plot

def draw_plot(instance,solution,title):
    x = []
    y = []
    solution.append(solution[0])
    for i in range(instance.dimension):
        x.append(instance.node_coords[i+1][0])
        y.append(instance.node_coords[i+1][1])
    for i in range(len(solution)-1):
        plot.plot(x,y,'ro')
        plot.plot([x[solution[i]-1],x[solution[i+1]-1]],[y[solution[i]-1],y[solution[i+1]-1]],'k-')
        plot.title(title)
    solution.pop()
    plot.show()
