################################################################################################################################

using DelimitedFiles
using JSON
using Random
using Printf
using DataStructures

################################################################################################################################

function evaluate_solution(solution::Vector{Int}, distance_matrix::Matrix{Float64})
    """Evaluate solution counting its total distance"""

    total_distance = 0
    for i in 1:length(solution)-1
        total_distance += distance_matrix[solution[i], solution[i+1]]
    end
    total_distance += distance_matrix[solution[length(solution)], solution[1]]

    return total_distance
end

################################################################################################################################

function generate_combinations(lists)
    """Generate all combiantions of selected parameters"""
    if length(lists) == 1
        return [[x] for x in lists[1]]
    else
        subcombinations = generate_combinations(lists[2:end])
        combinations = []
        for x in lists[1]
            for subcombination in subcombinations
                push!(combinations, [x, subcombination...])
            end
        end
        return combinations
    end
end

################################################################################################################################

function invert(solution::Vector{Int}, i::Int, j::Int)
    """Return solution with inverted elements between indexes i and j (inslusive)"""

    return vcat(solution[1:i-1],reverse(solution[i:j]),solution[j+1:end])
end

function swap(solution::Vector{Int}, i::Int, j::Int)
    solution[i], solution[j] = solution[j], solution[i]
    return solution
end

################################################################################################################################

function random(distance_matrix::Matrix{Float64})
    """Return distance, time and memory for random solution"""

    _, time, memory = @timed begin
        size = Int(sqrt(length(distance_matrix)))
        solution = randperm(size)
        distance = evaluate_solution(solution, distance_matrix)
    end

    return distance, time, memory
end

################################################################################################################################

function nearest_neighbor(start_node::Int, distance_matrix::Matrix{Float64})
    """Return distance, time and memory for nearest neighbor solution with specific start node"""

    size = Int(sqrt(length(distance_matrix)))
    solution = [start_node]
    for _ in 1:size-1
        current_node = last(solution)
        best_node = -1
        best_weight = Inf

        for node in 1:size
            if node ∉ solution
                weight = distance_matrix[current_node, node]
                if  weight < best_weight
                    best_weight = weight
                    best_node = node
                end
            end
        end

        push!(solution, best_node)

    end

    return solution, evaluate_solution(solution, distance_matrix)
end

################################################################################################################################

function extended_nearest_neighbor(distance_matrix::Matrix{Float64})
    """Return distance, time and memory for extedned nearest neighbor solution"""

    size = Int(sqrt(length(distance_matrix)))
    
    _, time, memory = @timed begin

        best_distance = Inf

        for node in 1:size
            _, distance = nearest_neighbor(node, distance_matrix)

            if distance < best_distance
                best_distance = distance
            end

        end
    end 

    return best_distance, time, memory
end

################################################################################################################################

function two_opt(distance_matrix::Matrix{Float64}, inital_solution::Vector{Int}, operator::Int)
    """Returns distance, time and memory for 2-opt solution"""
    
    size = Int(sqrt(length(distance_matrix)))

    _, time, memory = @timed begin

        best_solution = inital_solution
        best_distance = evaluate_solution(best_solution, distance_matrix)
        has_improved = true

        while has_improved
            has_improved = false
            current_solution = best_solution
            for i in 1:size-1
                for j in i+1:size

                    if operator == 1
                        new_solution = swap(copy(current_solution), i, j)
                    elseif operator == 2
                        new_solution = invert(current_solution, i, j)
                    end
                    new_distance = evaluate_solution(new_solution, distance_matrix)

                    if new_distance < best_distance
                        best_solution = new_solution
                        best_distance = new_distance
                        has_improved = true
                    end

                end
            end
        end

    end

    return best_distance, time, memory
end


################################################################################################################################

function tabu_search(distance_matrix::Matrix{Float64}, inital_solution::Vector{Int}, tabu_length::Int, operator::Int, iterations::Int)
    """Returns distance, time and memory for tabu search solution with specific tabu list length"""

    size = Int(sqrt(length(distance_matrix)))

    _, time, memory = @timed begin

        best_solution = inital_solution
        best_distance = evaluate_solution(best_solution, distance_matrix)
        best_distance_ever = best_distance
        best_ij = (0,0)
        tabu_list = []
        iter = 0
        has_improved = false
        
        while iter < iterations || has_improved == true
            iter = iter + 1
            has_improved = false
            current_solution = best_solution
            current_distance = best_distance
            best_distance = Inf
            for i in 1:size-1
                for j in i+1:size
                    if operator == 1
                        new_solution = swap(copy(current_solution), i, j)
                    elseif operator == 2
                        new_solution = invert(current_solution, i, j)   
                    end
                    new_distance = evaluate_solution(new_solution, distance_matrix)
                    if (i,j) in tabu_list && new_distance >= best_distance_ever
                        continue
                    end
                    if new_distance < best_distance && new_distance != current_distance
                        best_solution = new_solution
                        best_distance = new_distance
                        best_ij = (i,j)
                    end
                end
            end

            if best_distance < best_distance_ever
                best_distance_ever = best_distance
            end

            if best_distance < current_distance
                has_improved = true
            end

            push!(tabu_list, best_ij)

            if length(tabu_list) > tabu_length
                deleteat!(tabu_list, 1)
            end            
        end
    end

    return best_distance_ever, time, memory
end

################################################################################################################################

function generate_solutions(distance_matrix::Matrix{Float64}, pheromone_levels::Matrix{Float64}, ants::Int, alpha::Int, beta::Int)
    """Return solutions generated by specific number of ants"""

    size = Int(sqrt(length(distance_matrix)))
    solutions = Vector{Vector{Int}}()

    for _ in 1:ants

        current_node = rand(1:size)  
        solution = [current_node]

        unvisited_nodes = Set(1:size)
        delete!(unvisited_nodes, current_node)

        while length(unvisited_nodes) > 0
            probabilities = calculate_probabilities(current_node, unvisited_nodes, pheromone_levels, distance_matrix, alpha, beta)
            next_node = select_next_node(unvisited_nodes, probabilities)
            push!(solution, next_node)
            delete!(unvisited_nodes, next_node)
            current_node = next_node
        end

        push!(solutions, solution)
    end

    return solutions
end

function calculate_probabilities(
        current_node::Int, 
        unvisited_nodes::Set{Int}, 
        pheromone_levels::Matrix{Float64}, 
        distance_matrix::Matrix{Float64},
        alpha::Int,
        beta::Int
    )
    """Return list of probabilities for every node"""

    probabilities = Dict{Int, Float64}()
    total_probability = 0.0

    for node in unvisited_nodes
        pheromone = pheromone_levels[current_node, node]
        distance = distance_matrix[current_node, node]
        probability = pheromone^alpha * (1/distance)^beta
        probabilities[node] = probability
        total_probability += probability
    end

    for node in keys(probabilities)
        probabilities[node] /= total_probability
    end

    return probabilities
end

function select_next_node(unvisited_nodes, probabilities)
    """Return selected node based on probabilities"""

    r = rand()
    cumulative_probability = 0.0
    
    for node in unvisited_nodes

        cumulative_probability += probabilities[node]

        if cumulative_probability >= r
            return node
        end
    end
    return first(unvisited_nodes)
end

function update_pheromone_levels(
        pheromone_levels::Matrix{Float64}, 
        solutions::Vector{Vector{Int}}, 
        evaporation_rate::Int, 
        distance_matrix::Matrix{Float64}
    )
    """Update pheromone level for every pair of nodes"""

    size = Int(sqrt(length(distance_matrix)))


    for solution in solutions

        pheromone_to_deposit = 1 / evaluate_solution(solution, distance_matrix)  

        for i in 1:(size-1)
            pheromone_levels[solution[i], solution[i+1]] += pheromone_to_deposit
            pheromone_levels[solution[i+1], solution[i]] += pheromone_to_deposit 
        end

        pheromone_levels[solution[end], solution[1]] += pheromone_to_deposit
        pheromone_levels[solution[1], solution[end]] += pheromone_to_deposit  
    end

    pheromone_levels *= (1-evaporation_rate/100)

end

function ant_colony(distance_matrix::Matrix{Float64}, iterations::Int, ants::Int, evaporation_rate::Int, alpha::Int, beta::Int, start::Int)
    """Returns distance, time and memory for ant colony solution"""

    size = Int(sqrt(length(distance_matrix)))

    _, time, memory = @timed begin
        
        if start == 1
            pheromone_levels = ones(size, size)
        elseif start == 2
            pheromone_levels = rand(size, size)
        end

        solutions = Vector{Vector{Int}}()
        best_distance_ever = Inf

        for _ in 1:iterations
            solutions = generate_solutions(distance_matrix, pheromone_levels, ants, alpha, beta)
            update_pheromone_levels(pheromone_levels, solutions, evaporation_rate, distance_matrix)
            best_distance = evaluate_solution(sort(solutions, by=x->evaluate_solution(x, distance_matrix))[1], distance_matrix)
            if best_distance < best_distance_ever
                best_distance_ever = best_distance
            end
        end

    end

    return best_distance_ever, time, memory
end

################################################################################################################################

function simulated_annealing(distance_matrix::Matrix{Float64}, initial_temperature::Int, cooling_rate::Int, iterations::Int)
    """Returns distance, time and memory for simulated annealing solution"""

    size = Int(sqrt(length(distance_matrix)))

    _, time, memory = @timed begin

        best_solution = randperm(size)
        best_distance = evaluate_solution(best_solution, distance_matrix)

        current_solution = best_solution
        current_distance = evaluate_solution(current_solution, distance_matrix)
        best_distance = current_distance
        temperature = initial_temperature

        for iteration in 1:iterations

            i, j = rand(1:size, 2)
            neighbor_solution = swap(copy(current_solution), i, j)
            neighbor_distance = evaluate_solution(neighbor_solution, distance_matrix)

            distance_difference = neighbor_distance - current_distance

            if distance_difference < 0 || rand() < exp(-distance_difference / temperature)

                current_solution = neighbor_solution
                current_distance = neighbor_distance
                
                if current_distance < best_distance
                    best_distance = current_distance
                end
            end

            temperature *= cooling_rate/100
        end
    end

    return best_distance, time, memory
end

################################################################################################################################

function get_results(repetitions::Int, distance_matrix::Matrix{Float64}, algorithm::Function, initial_solutions::Vector{Vector{Int}})
    """Get average results (of some repetitions) for specific instance and algorithm"""
    size = Int(sqrt(length(distance_matrix)))
    best_distance = Inf

    total_distance = 0
    total_time = 0
    total_memory = 0

    if algorithm == extended_nearest_neighbor
        distance, time, memory = algorithm(distance_matrix)
        return distance, distance, time, memory
    end

    for i in 1:repetitions
        if algorithm == tabu_search
            distance, time, memory = tabu_search(distance_matrix, initial_solutions[i], 10, 2, 70)
        elseif algorithm == ant_colony
            distance, time, memory = ant_colony(distance_matrix, 10, 20, 35, 1, 5)
        elseif algorithm == simulated_annealing
            distance, time, memory = simulated_annealing(distance_matrix, 1000000, 99, 100000)
        elseif algorithm == two_opt
            distance, time, memory = two_opt(distance_matrix, initial_solutions[i], 2)
        else 
            distance, time, memory = algorithm(distance_matrix)
        end 

        total_distance += distance
        total_time += time
        total_memory += memory

        if (distance < best_distance)
            best_distance = distance
        end

    end
    return best_distance, total_distance/repetitions, total_time/repetitions, total_memory/repetitions
end

function get_results2(repetitions::Int, distance_matrix::Matrix{Float64}, algorithm::Function, combination::Vector{Int})
    """Get average results (of some repetitions) for specific instance and combination of parameters"""

    size = Int(sqrt(length(distance_matrix)))
    best_distance = Inf

    total_distance = 0
    total_time = 0
    total_memory = 0

    for i in 1:repetitions
        
        if algorithm == tabu_search || algorithm == two_opt
            distance, time, memory = algorithm(distance_matrix, randperm(size), combination...)
        else
            distance, time, memory = algorithm(distance_matrix, combination...)
        end

        total_distance += distance
        total_time += time
        total_memory += memory

        if (distance < best_distance)
            best_distance = distance
        end

    end
    return best_distance, total_distance/repetitions, total_time/repetitions, total_memory/repetitions
end

function get_results3(repetitions::Int, distance_matrix::Matrix{Float64}, algorithm::Function, params::String, initial_solutions::Vector{Vector{Int}})
    """Get average results (of some repetitions) for specific instance and algorithm with specified parameters"""
    size = Int(sqrt(length(distance_matrix)))
    best_distance = Inf

    total_distance = 0
    total_time = 0
    total_memory = 0

    if algorithm == extended_nearest_neighbor
        distance, time, memory = algorithm(distance_matrix)
        return distance, distance, time, memory
    end

    for i in 1:repetitions

        if algorithm == random
            distance, time, memory = algorithm(distance_matrix)
        elseif algorithm == tabu_search || algorithm == two_opt
            params_arr = split(params, ',')
            parameters = parse.(Int, params_arr)
            distance, time, memory = algorithm(distance_matrix, initial_solutions[i], parameters...)
        else
            params_arr = split(params, ',')
            parameters = parse.(Int, params_arr)
            distance, time, memory = algorithm(distance_matrix, parameters...)
        end 

        total_distance += distance
        total_time += time
        total_memory += memory

        if (distance < best_distance)
            best_distance = distance
        end

    end
    return best_distance, total_distance/repetitions, total_time/repetitions, total_memory/repetitions
end


################################################################################################################################

function main()
    """Read instance_file, for every algorithm get average results and save everything to results_file"""
    option = ARGS[1]

    if option == "comparison"
        filepath = ARGS[2] 
        file = open(filepath, "r")

        type = readline(file)
        size = parse(Int, readline(file))
        range = parse(Int, readline(file))

        distance_matrix = DelimitedFiles.readdlm(file, ' ')  
        size = Int(sqrt(length(distance_matrix)))

        close(file)

        path_components = splitpath(filepath)
        path_components[end] = string("results_", path_components[end][1:end-4], ".txt")
        filepath = joinpath(path_components...)

        repetitions = parse(Int, ARGS[3]) 

        file = open(filepath, "w")

        write(file, type * "\n")
        write(file, string(size) * "\n")
        write(file, string(range) * "\n")
        write(file, string(repetitions) * "\n")
        initial_solutions = [randperm(size) for _ in 1:repetitions]
        for algorithm in [random, extended_nearest_neighbor, two_opt, tabu_search, ant_colony, simulated_annealing]
            best_distance, average_distance, average_time, average_memory = get_results(repetitions, distance_matrix, algorithm, initial_solutions)
            write(file, string(algorithm) * " " * string(average_distance) * " " * string(average_time*1000) * " " * string(average_memory/1024) * " " * string(best_distance) * "\n")
        end
        write(file, '\n')

################################################################################################################################

    elseif option == "parameters"

        parameters_file = ARGS[2] 
        file = open(parameters_file, "r")
        parameters = OrderedDict{String, Vector{Int}}()
        for line in eachline(file)
            words = split(line)
            merge!(parameters, Dict(words[1]=>[]))
            for i in 2:length(words)
                push!(parameters[words[1]], parse(Int, words[i]))
            end
        end
        close(file)

        instance_file = ARGS[3]
        file = open(instance_file, "r")
        type = readline(file)
        size = parse(Int, readline(file))
        range = parse(Int, readline(file))
        distance_matrix = DelimitedFiles.readdlm(file, ' ')  
        close(file)
        
        path_components = splitpath(instance_file)
        path_components[end] = string("results_", path_components[end][1:end-4], ".txt")
        results_file = joinpath(path_components...)
        
        repetitions = parse(Int, ARGS[4]) 

        parameters_values = Vector{Vector{Int}}()
        for parameter in keys(parameters)
            values = Vector{Int}()
            for i in 1:length(parameters[parameter])
                push!(values, parameters[parameter][i])
            end
            push!(parameters_values, values)
        end
        combinations = generate_combinations(parameters_values)

        algorithm = Function
        if ARGS[5] == "two_opt"
            algorithm = two_opt
        elseif ARGS[5] == "tabu_search"
            algorithm = tabu_search
        elseif ARGS[5] == "ant_colony"
            algorithm = ant_colony
        elseif ARGS[5] == "simulated_annealing"
            algorithm = simulated_annealing
        end

        file = open(results_file, "w")
        
        write(file, type * "\n")
        write(file, string(size) * "\n")
        write(file, string(range) * "\n")
        write(file, string(repetitions) * "\n")
        for combination in combinations
            best_distance, average_distance, average_time, average_memory = get_results2(repetitions, distance_matrix, algorithm, combination)
            write(file, join(combination, ",") * " " * string(average_distance) * " " * string(average_time*1000) * " " * string(average_memory/1024) * " " * string(best_distance) * "\n")
        end
        write(file, '\n')

################################################################################################################################

    elseif option == "third"

        filepath = ARGS[2] 
        file = open(filepath, "r")

        type = readline(file)
        size = parse(Int, readline(file))
        range = parse(Int, readline(file))

        distance_matrix = DelimitedFiles.readdlm(file, ' ')  

        close(file)

        path_components = splitpath(filepath)
        path_components[end] = string("results_", path_components[end][1:end-4], ".txt")
        filepath = joinpath(path_components...)

        repetitions = parse(Int, ARGS[3]) 

        file = open(filepath, "w")
        
        optimal_parameters = Dict()
        for algorithm in ["two_opt", "tabu_search", "ant_colony", "simulated_annealing"]
            if ! isfile(joinpath(ARGS[4], algorithm * "_optimal.txt"))
                println("Error: There is no file with optimal parameters\n")
                return 
            end
            optimal_parameters[algorithm] = JSON.parsefile(joinpath(ARGS[4], algorithm * "_optimal.txt"))
        end
        write(file, type * "\n")
        write(file, string(size) * "\n")
        write(file, string(range) * "\n")
        write(file, string(repetitions) * "\n")
        initial_solutions = [randperm(size) for _ in 1:repetitions]
        for algorithm in [random, extended_nearest_neighbor, two_opt, tabu_search, ant_colony, simulated_annealing]
            algorithm_string = string(algorithm)
            configuration = "('$type', '$size', '$range')"
            if algorithm != random && algorithm != extended_nearest_neighbor
                parameters = optimal_parameters[algorithm_string][configuration]
            else
                parameters = ""
            end
            best_distance, average_distance, average_time, average_memory = get_results3(repetitions, distance_matrix, algorithm, parameters, initial_solutions)
            write(file, string(algorithm) * " " * string(average_distance) * " " * string(average_time*1000) * " " * string(average_memory/1024) * " " * string(best_distance) * "\n")
        end
        write(file, '\n')
    end
end

################################################################################################################################

main()
 
################################################################################################################################
