import argparse
import pandas as pd

from helpers import (
    compute_route_distance,
    get_distance,
    compute_freezing_temperature
)

from neighbor import (
    basic_nearest_neighbor
)

from simulated_anneal import (
    simulated_annealing
)

from visualization import (
    plot_convergence,
    plot_route,
    plot_route_comparison
)

# ========================================== Args ==========================================

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input",
    required=True,
    type=str,
    help="Path to input .csv file",
)

parser.add_argument(
    "-d",
    "--distance_type",
    choices=['euclidean', 'manhattan'],
    default='euclidean',
    help="Select distance type",
)

parser.add_argument(
    "-r",
    "--random_type",
    choices=['swap', 'reverse'],
    default='swap',
    help="Select distance type",
)

args = parser.parse_args()

file = args.input
name = file.split('.')[0]
name = name.split('/')[1]
name = "outputs/" + name

# ========================================== Load Cities ==========================================

df = pd.read_csv(file, names=["x", "y"])

cities = [(pos, tuple(row)) for pos, row in df.iterrows()]

# ========================================== Distance Matrix ==========================================

distance_matrix = {}

for index1, position1 in cities:

    distance_matrix[index1] = {}

    for index2, position2 in cities:

        distance_matrix[index1][index2] = get_distance(
            position1,
            position2,
            distance_type = args.distance_type
        )

# ========================================== Initial Solution ==========================================

initial_route = basic_nearest_neighbor(
    cities,
    distance_matrix
)

initial_distance = compute_route_distance(
    initial_route,
    distance_matrix
)

print("Initial Route:", initial_route)
print("Initial Distance:", initial_distance)

# ========================================== Simulated Annealing ==========================================

estimated_freezing_temperature = compute_freezing_temperature(
    best_distance=initial_distance,
    neighbor_distance=initial_distance + 10,
    v=5
)

print("estimated_freezing_temperature", estimated_freezing_temperature)
best_route, best_distance, history = simulated_annealing(
    initial_route=initial_route,
    distance_matrix=distance_matrix,
    initial_temperature=10,
    cooling_rate=0.99995,
    stopping_temperature=estimated_freezing_temperature,
    random_type=args.random_type,
    max_iterations=100000000
)

print("Best Route:", best_route)
print("Best Distance:", best_distance)

# ========================================== Visualizations ==========================================

plot_convergence(
    history,
    output_file= name + "_convergence.png"
)

plot_route(
    initial_route,
    cities,
    title="Initial Nearest Neighbor Route",
    output_file=name + "_initial_route.png"
)

plot_route(
    best_route,
    cities,
    title="Final Simulated Annealing Route",
    output_file= name + "_final_route.png"
)

plot_route_comparison(
    initial_route,
    best_route,
    cities,
    output_file= name + "_route_comparison.png"
)


print(
    "size: ", len(cities),
    "initial_distance: ", initial_distance,
    "best_distance: ", best_distance
)