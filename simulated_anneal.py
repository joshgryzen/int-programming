import math
import random

from helpers import compute_route_distance


# ========================================== Simulated Annealing ==========================================

# https://www.fourmilab.ch/documents/travelling/anneal/

# swap 2 random 
def generate_neighbor_by_swapping(route):

    neighbor_route = route.copy()

    index1 = random.randint(1, len(route) - 2)
    index2 = random.randint(1, len(route) - 2)

    while index1 == index2:
        index2 = random.randint(1, len(route) - 2)

    neighbor_route[index1], neighbor_route[index2] = (
        neighbor_route[index2],
        neighbor_route[index1]
    )

    return neighbor_route

# select random continuous sublist (except for first and last) and reverse it
def generate_neighbor_by_reverse(route):
    neighbor_route = route.copy()

    # Pick two random internal indices
    idx1 = random.randint(1, len(neighbor_route) - 2)
    idx2 = random.randint(1, len(neighbor_route) - 2)

    # Ensure start <= end
    start, end = sorted([idx1, idx2])

    # Reverse subsequence
    neighbor_route[start:end + 1] = neighbor_route[start:end + 1][::-1]

    return neighbor_route

def acceptance_probability(current_distance, neighbor_distance, temperature):

    if neighbor_distance < current_distance:
        return 1.0

    delta = neighbor_distance - current_distance

    return math.exp(-delta / temperature)

def update_temperature(temperature, cooling_rate):

    return temperature * cooling_rate

def simulated_annealing(initial_route, distance_matrix, initial_temperature, cooling_rate, stopping_temperature, max_iterations, random_type):

    current_route = initial_route.copy()

    current_distance = compute_route_distance(current_route, distance_matrix)

    best_route = current_route.copy()
    best_distance = current_distance

    temperature = initial_temperature

    iteration = 0

    history = [best_distance]

    while (temperature > stopping_temperature and iteration < max_iterations):

        if random_type == "swap":
            neighbor_route = generate_neighbor_by_swapping(current_route)

        else:
            neighbor_route = generate_neighbor_by_reverse(current_route)

        neighbor_distance = compute_route_distance(neighbor_route, distance_matrix)

        probability = acceptance_probability(current_distance, neighbor_distance, temperature)

        if probability > random.random():
            current_route = neighbor_route
            current_distance = neighbor_distance

        if current_distance < best_distance:
            best_route = current_route.copy()
            best_distance = current_distance

        history.append(best_distance)

        temperature = update_temperature(temperature, cooling_rate)

        iteration += 1

    return best_route, best_distance, history