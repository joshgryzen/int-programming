import pandas as pd
import math

def get_neighbor(remaining_cities, visited, current_index, current_position, distance_matrix):
    distance = math.inf
    closest_neighbor = current_index
    closest_position = current_position

    for next_index, next_position in remaining_cities:
        if next_index in visited or current_index == next_index:
            continue

        # distance lookup
        neighbor_distance = distance_matrix[current_index][next_index]

        if distance > neighbor_distance:
            distance = neighbor_distance
            closest_neighbor = next_index
            closest_position = next_position

    return closest_neighbor, closest_position


# ========================================== Basic Nearest Neighbor ==========================================

# Start at the first node
# Find the closest unvisted node and travel there
# Repeat until all nodes are visted

def get_route(current_index, current_position, visited, remaining_cities, distance_matrix):

    # sets are faster?
    visited_set = set(visited)

    while remaining_cities:

        closest_neighbor, closest_position = get_neighbor(remaining_cities, visited_set, current_index, current_position, distance_matrix)
        visited.append(closest_neighbor)
        visited_set.add(closest_neighbor)

        # distances.append(distance)

        remaining_cities.remove((closest_neighbor, closest_position))

        current_index = closest_neighbor
        current_position = closest_position

    # go back to the start now
    # visited.append(0)
    
    return visited

def basic_nearest_neighbor(cities, distance_matrix):

    initial_index, initial_position = cities[0]
    remaining_cities = cities[1:]
    route = get_route(initial_index, initial_position, [initial_index], remaining_cities, distance_matrix)
    
    return route