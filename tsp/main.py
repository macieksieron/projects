################################################################################################################################

import random
import math
import subprocess
import os
import json
import glob 
import pandas
import matplotlib.pyplot as plt

################################################################################################################################

def find_lowest_level_directories(root_dir):
    """Return list of all subdirectories of root_dir, which does not have any subdirectories"""
    lowest_level_dirs = []

    for dirpath, dirnames, _ in os.walk(root_dir):
        if not dirnames: 
            lowest_level_dirs.append(dirpath)

    return lowest_level_dirs

################################################################################################################################

def d(x1, y1, x2, y2):
  """Calculate euclidean distance of 2 points: (x1, y1) and (x2, y2)"""
  y = y1 - y2
  x = x1 - x2
  return math.sqrt(y*y+x*x)

################################################################################################################################

def PRD(distance, optimal):
    """Calculate PRD of some solution's distance"""
    return ((distance - optimal) / optimal) * 100
        
################################################################################################################################

def generate_single_instance(size, type, _range, name):
    """Generate instance with specific parameters and save it to file"""
    distance_matrix = [[0 for _ in range(size)] for _ in range(size)]
    if type == "euclidean":
                print(f"Generating euclidean instance {name} of size {size}")
                point_range = _range/math.sqrt(2)
                points = [(random.uniform(1, point_range), random.uniform(1, point_range)) for _ in range(size)]
                for i in range(size):
                    for j in range(size):
                        distance_matrix[i][j] = d(points[i][0],points[i][1],points[j][0],points[j][1])
    elif type == "symmetric":
        print(f"Generating symmetric instance {name} of size {size}")
        for i in range(size):
            for j in range(i,size):
                if i != j:
                    distance_matrix[i][j] = distance_matrix[j][i] = random.randint(1,_range)
    elif type == "asymmetric":
        print(f"Generating asymmetric instance {name} of size {size}")
        for i in range(size):
            for j in range(size):
                if i != j:
                    distance_matrix[i][j] = random.randint(1, _range)
    else:
        print(f"Error: \"{type}\" is wrong type of instance")
        return

    with open(f"{name}.txt", 'w') as file:
            file.writelines("\n".join([
                type, 
                str(size),
                str(_range)
            ]))
            file.write("\n")
            for row in distance_matrix:
                file.write(" ".join(map(str,row)))
                file.write("\n")

################################################################################################################################

print("1.Generate set of instances")
print("2.Test parameters")
print("3.Compare algorithms")
print("4.Create excel")
print("5.Save optimal parameters")
print("6.Compare algorithms with parameters")
print("7.Plot results")
answer = input()

parameters = {
    "two_opt": ["operator"],
    "tabu_search": ["tabu_lenght", "operator", "iterations"],
    "ant_colony": ["iterations", "ants", "evaporation_rate", "alpha", "beta", "start"],
    "simulated_annealing": ["initial_temperature", "cooling_rate", "iterations"]
}

################################################################################################################################

if answer == "1":
    print("Name: ", end="")
    name = input()

    if os.path.isdir(name):
        print("Error: Set of instances with this name already exists!")
    else:
        print("Types: ", end="")
        types = input().split()
        print("Sizes: ", end="")
        sizes = input().split()
        print("Ranges: ", end="")
        ranges = input().split()
        print("Number of instances for each setting: ", end="")
        number_of_instances_for_each_setting = int(input())

        os.mkdir(name)

        for type in types:
            os.mkdir(os.path.join(name, type))
            for size in sizes:
                os.mkdir(os.path.join(name, type, size))
                for _range in ranges: 
                    os.mkdir(os.path.join(name, type, size, _range))
                    for i in range(1, number_of_instances_for_each_setting+1):
                        generate_single_instance(
                            int(size),
                            type,
                            int(_range),
                            os.path.join(name, type, size, _range, f"instance{i}")
                        )
################################################################################################################################

elif answer == "2":

    print("Instance set name: ", end="")
    name = input()
    print("Number of repetitions for each instance: ", end="")
    repetitions = input()
    print("Algorithm: ", end="")
    algorithm = input()
    print()

    if algorithm in parameters:
        selected_parameters = {selected_parameter: [] for selected_parameter in parameters[algorithm]}
        for parameter in selected_parameters:
            print(f"{parameter}: ", end="")
            selected_parameters[parameter] = [option for option in input().split()]
            parameters_file = os.path.join(name, f"{algorithm}.txt")
            with open(parameters_file, 'w') as f:
                for p in selected_parameters:
                    f.write(f"{p} ")
                    for value in selected_parameters[p]:
                        f.write(f"{value} ")
                    f.write('\n')
        
        for instance_file in glob.glob(os.path.join(name, '**/instance*.txt'), recursive=True):
            subprocess.run(["julia", "algorithms.jl", "parameters", parameters_file, instance_file, repetitions, algorithm])
            print(f"{instance_file} solution calculated {repetitions} times. Average results saved to file.")

        for directory in find_lowest_level_directories(name):
            result_files = glob.glob(os.path.join(directory, 'results_*.txt'))
            combinations = []
            with open(result_files[0], 'r') as f:
                lines = f.readlines()[4:-1]
                for line in lines:
                    combinations.append(line.split()[0])
            f.close()
            sums = {combination: [0.0, 0.0, 0.0, 0.0, float('inf')] for combination in combinations}
            for result_file in result_files:
                with open(result_file, "r") as file:
                    lines = file.readlines()[4:-1] # skip first 4 lines (instance description) and last line (newline)
                optimum = float('inf')
                for line in lines:
                    _, _, _, _, best = line.split(" ")
                    best = float(best[:-1])
                    if best < optimum:
                        optimum = best

                for line in lines:
                    combination, distance, time, memory, best_distance = line.split(" ")
                    best_distance = float(best_distance[:-1])
                    if best_distance < sums[combination][4]:
                        sums[combination][4] = best_distance
                    sums[combination][0] += float(distance)
                    sums[combination][1] += float(time)
                    sums[combination][2] += float(memory)
                    sums[combination][3] += PRD(float(distance), optimum)

            for combination in sums:
                sums[combination][4] = sums[combination][4] * len(result_files)

            with open(os.path.join(directory, "averages.txt"), "w") as file:
                file.write(os.path.basename(os.path.dirname(os.path.dirname(directory))))
                file.write("\n")
                file.write(os.path.basename(os.path.dirname(directory)))
                file.write("\n")
                file.write(os.path.basename(directory))
                file.write("\n")
                for combination in sums:
                    file.write(combination + " " + " ".join(map(lambda x: str(x/len(result_files)), sums[combination])) + "\n")
            print(f"{directory} averages saved to file!")
    else:
        print("Error: Algorithm does not exists or doesn't have any parameters to test")

################################################################################################################################

elif answer == "3" or answer == "6":
    print("Instance set name: ", end="")
    name = input()
    print("Number of repetitions for each instance: ", end="")
    repetitions = input()
    print()

    if answer == "3":
        for instance_file in glob.glob(os.path.join(name, '**/instance*.txt'), recursive=True):
            subprocess.run(["julia", "algorithms.jl", "comparison", instance_file, repetitions])
            print(f"{instance_file} solution calculated {repetitions} times. Average results saved to file.")
    if answer == "6":
        for instance_file in glob.glob(os.path.join(name, '**/instance*.txt'), recursive=True):
            subprocess.run(["julia", "algorithms.jl", "third", instance_file, repetitions, name])
            print(f"{instance_file} solution calculated {repetitions} times. Average results saved to file.")

    for directory in find_lowest_level_directories(name):
        result_files = glob.glob(os.path.join(directory, 'results_*.txt'))
        sums = {algorithm: [0.0, 0.0, 0.0, 0.0, float('inf')] for algorithm in ["random", "extended_nearest_neighbor", "two_opt", "tabu_search", "ant_colony", "simulated_annealing"]}
        for result_file in result_files:
            with open(result_file, "r") as file:
                lines = file.readlines()[4:-1] # skip first 4 lines (instance description) and last line (newline)

            optimum = float('inf')
            for line in lines:
                _, _, _, _, best = line.split(" ")
                best = float(best[:-1])
                if best < optimum:
                    optimum = best

            for line in lines:
                algorithm, distance, time, memory, best_distance = line.split(" ")
                best_distance = float(best_distance[:-1]) # delete "\n" from last word in line
                if best_distance < sums[algorithm][4]:
                    sums[algorithm][4] = best_distance
                sums[algorithm][0] += float(distance)
                sums[algorithm][1] += float(time)
                sums[algorithm][2] += float(memory)
                sums[algorithm][3] += PRD(float(distance), optimum)

        for combination in sums:
            sums[combination][4] = sums[combination][4] * len(result_files)

        with open(os.path.join(directory, "averages.txt"), "w") as file:
            file.write(os.path.basename(os.path.dirname(os.path.dirname(directory))))
            file.write("\n")
            file.write(os.path.basename(os.path.dirname(directory)))
            file.write("\n")
            file.write(os.path.basename(directory))
            file.write("\n")
            for algorithm in sums:
                file.write(algorithm + " " + " ".join(map(lambda x: str(x/len(result_files)), sums[algorithm])) + "\n")
        print(f"{directory} averages saved to file!")

################################################################################################################################

elif answer == "4":
    print("Instance set name: ", end="")
    name = input()

    results = {}
    for lowest_dir in find_lowest_level_directories(name):
        with open(os.path.join(lowest_dir, "averages.txt")) as f:
            type = f.readline()[:-1]
            size = f.readline()[:-1]
            range = f.readline()[:-1]
            for line in f.readlines():
                algorithm, distance, time, memory, prd, best_distance = line.split(" ")
                if (type, size, range) not in results:
                    results[(type, size, range)] = []
                results[(type, size, range)].append((algorithm, distance, time, memory, prd, best_distance))
    dataframes = []
    for i in [1,2,3,4,5]:
        data = {}
        for configuration in results:
            for result in results[configuration]:
                if result[0] not in data:
                    data[result[0]] = []
                data[result[0]].append(float(result[i]))

        index = list(results)
        dataframes.append(pandas.DataFrame(data, index=index))

    excel_file = f"{name}.xlsx"
    with pandas.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        for i, df in enumerate(dataframes):
            df.to_excel(writer, sheet_name=str(i))
                  
################################################################################################################################

elif answer == "5":
    print("Instance set name: ", end="")
    name = input()
    print("Algorithm: ",  end="")
    algorithm = input()
    results = {}
    for lowest_dir in find_lowest_level_directories(name):
        with open(os.path.join(lowest_dir, "averages.txt")) as f:
            type = f.readline()[:-1]
            size = f.readline()[:-1]
            range = f.readline()[:-1]
            for line in f.readlines():
                combination, distance, time, memory, prd, best = line.split(" ")
                if (type, size, range) not in results:
                    results[(type, size, range)] = []
                results[(type, size, range)].append((combination, distance, time, memory, prd, best))
    data = {}

    for configuration in results:
        best_prd = float('inf')
        best_parameters = ""
        for result in results[configuration]:
            if float(result[4]) < best_prd:
                best_prd = float(result[4])
                best_parameters = result[0]
        data[str(configuration)] = best_parameters
    with open(f"{algorithm}_optimal.txt", 'w') as f:
        json.dump(data, f)

################################################################################################################################

# CUSTOMIZE FOR EVERY XLSX FILE
elif answer == "7":
    print("Instance set name: ", end="")
    name = input()

    excel_file = f'{name}.xlsx'
    columns = ["10,50,20,1,2,1",	"10,50,20,1,2,2",	"10,50,20,1,5,1",	"10,50,20,1,5,2",
                "10,50,20,1,10,1",	"10,50,20,1,10,2",	"10,50,50,1,2,1",	"10,50,50,1,2,2",	"10,50,50,1,5,1",	"10,50,50,1,5,2",	"10,50,50,1,10,1",	"10,50,50,1,10,2",	"10,50,80,1,2,1",	"10,50,80,1,2,2",
                "10,50,80,1,5,1",	"10,50,80,1,5,2",	"10,50,80,1,10,1",	"10,50,80,1,10,2",	"10,50,90,1,2,1",	"10,50,90,1,2,2",
                "10,50,90,1,5,1",	"10,50,90,1,5,2",	"10,50,90,1,10,1",	"10,50,90,1,10,2"]

    # cols = ["2","4","8","16","32","64","128"]
    # cols = ["1", "2"]
    # cols = ["1000,20", "1000,80", "1000,90", "1000,99","10000,20", "10000,80", "10000,90", "10000,99","100000,20", "100000,80", "100000,90", "100000,99"]
    cols = ["random", "extended_nearest_neighbor", "two_opt", "tabu_search", "ant_colony", "simulated_annealing"]

    for i in range(5):

        df = pandas.read_excel(excel_file, sheet_name=str(i), header=None, names=['Instance_Size_Range']+cols)

        df[['Type', 'Size', 'Range']] = df['Instance_Size_Range'].str.extract(r"'(\w+)', '(\d+)', '(\d+)'")

        if i == 0:
            stat = "średni wynik"
        elif i == 1:
            stat = "średni czas"
        elif i == 2:
            stat = "średnie zużycie pamięci"
        elif i == 3:
            stat = "średnie PRD"
        elif i == 4:
            stat = "najlepszy wynik"

        for type in ["euclidean"]:
        
            data = df[df['Type'] == type]

            sizes = ["20", "40", "60", "80", "100"]
            # prefixes = ["20","80","90","99"]
            # prefixes = ["20", "80", "90", "99"]
            prefixes = ["extended_nearest_neighbor", "two_opt", "tabu_search", "ant_colony", "simulated_annealing"]
            result_lists = {prefix: [] for prefix in prefixes}

            for size in sizes:
                size_data = data[data['Size'] == size]
                for prefix in prefixes:
                    result_lists[prefix].append(sum([float(size_data[column].iloc[0]) for column in size_data.columns if column==prefix]))
            for j in prefixes:
                # plt.plot(sizes, result_lists[j], label=f'{"swap" if j=="1" else "invert"}-{type}')
                plt.plot(sizes, result_lists[j], label=f"{j}-{type}")
            # plt.plot(sizes, swaps, label=f"swap-{type}")
            # plt.plot(sizes, inverts, label=f"invert-{type}")
            plt.title("Porównanie algorytmów")
            plt.xlabel('rozmiar instancji')
            plt.ylabel(stat)
            # plt.legend(loc='upper left', bbox_to_anchor=(1,1))
            # plt.tight_layout()
            plt.legend()

        plt.savefig(os.path.join(name, "plots", type+"_"+stat))
        plt.close()
else:
    print("Error: Wrong menu option!")

################################################################################################################################

