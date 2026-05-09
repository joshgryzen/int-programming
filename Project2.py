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
    default='euclidean',
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

# ========================================== Basic Nearest Neighbor ==========================================

# Start at the first node
# Find the closest unvisted node and travel there
# Repeat until all nodes are visted

def get_next_neighbor(current_index, current_position, visited, distances, remaining_cities):
    closest_neighbor = current_index
    closest_position = current_position
    distance = math.inf
    for next_index, next_position in remaining_cities:
        if next_index in visited or current_index == next_index:
                continue
        neighbor_distance = get_distance(current_position, next_position)
        print("Distance from ", current_index, "to ", next_index, "is ", neighbor_distance)
        if distance > neighbor_distance:
            distance = neighbor_distance
            closest_neighbor = next_index
            closest_position = next_position
    visited.append(closest_neighbor)
    distances.append(distance)
    print(remaining_cities)
    remaining_cities.remove((closest_neighbor, closest_position))
    if remaining_cities:
         return get_next_neighbor(closest_neighbor, closest_position, visited, distances, remaining_cities)
    return visited, distances

initial_index, initial_position = cities.pop(0)
route, distances = get_next_neighbor(initial_index, initial_position, [initial_index], [0], cities)

# go back to the start now
final_position = df.iloc[route[-1]]
print(final_position)
final_distance = get_distance(initial_position, final_position)
distances.append(final_distance)
route.append(0)

print("Route: ", route)
print("Distances: ", distances)