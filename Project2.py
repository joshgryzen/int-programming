import argparse
import pandas as pd
import math

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
    default='manhattan',
    help="Select distance type: euclidean or manhattan",
)

args = parser.parse_args()
file = args.input
distance_type = args.distance_type

df = pd.read_csv(file, names=["x", "y"])

initial_node = df.iloc[0]

cities = [(pos, row.tolist()) for pos, row in df.iterrows()]

# ========================================== Helper Functions ==========================================
def get_distance(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    if distance_type == "euclidean":
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    else: 
        return abs(x2-x1) + abs(y2-y1)    

def get_neighbor(remaining_cities, visited, current_index, current_position):
    distance = math.inf
    closest_neighbor = current_index
    closest_position = current_position
    for next_index, next_position in remaining_cities:
        if next_index in visited or current_index == next_index:
                continue
        neighbor_distance = get_distance(current_position, next_position)
        # print("Distance from ", current_index, "to ", next_index, "is ", neighbor_distance)
        if distance > neighbor_distance:
            distance = neighbor_distance
            closest_neighbor = next_index
            closest_position = next_position
            
    return closest_neighbor, closest_position, distance

# ========================================== Basic Nearest Neighbor ==========================================

# Start at the first node
# Find the closest unvisted node and travel there
# Repeat until all nodes are visted

def get_route(current_index, current_position, visited, distances, remaining_cities):
    while remaining_cities:
        closest_neighbor, closest_position, distance = get_neighbor(remaining_cities, visited, current_index, current_position)
        visited.append(closest_neighbor)
        distances.append(distance)
        remaining_cities.remove((closest_neighbor, closest_position))
        current_index = closest_neighbor
        current_position = closest_position
    
    # go back to the start now
    final_position = df.iloc[visited[-1]]
    initial_position = df.iloc[visited[0]]
    print(final_position)
    final_distance = get_distance(final_position, initial_position)
    distances.append(final_distance)
    visited.append(0)
    return visited, distances

def basic_nearest_neighbor(cities):
    initial_index, initial_position = cities[0]
    remaining_cities = cities[1:]
    route, distances = get_route(initial_index, initial_position, [initial_index], [0], remaining_cities)

    print("Route: ", route)
    print("Distances: ", distances)
    total_distance = 0
    for distance in distances:
        total_distance += distance

    print("Total distance: ", total_distance)

# basic_nearest_neighbor(cities)
