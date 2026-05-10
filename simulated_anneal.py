import math
import random

from helpers import compute_route_distance


# ========================================== Simulated Annealing ==========================================

# Some resources
# https://www.fourmilab.ch/documents/travelling/anneal/
# https://sites.gatech.edu/omscs7641/2024/02/19/simulated-annealing-methods-and-real-world-applications/

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
    # print("Original route:", route)
    # print("Neighbor route:", neighbor_route)
    return neighbor_route

# select random continuous sublist (except for first and last) and reverse it
def generate_neighbor_by_reverse(route):
    neighbor_route = route.copy()

    # Pick two random internal indices
    idx1 = random.randint(1, len(neighbor_route) - 1)
    idx2 = random.randint(1, len(neighbor_route) - 1)

    # Ensure start <= end
    start, end = sorted([idx1, idx2])

    # Reverse subsequence
    neighbor_route[start:end + 1] = neighbor_route[start:end + 1][::-1]

    # print("Original route:", route)
    # print("Neighbor route:", neighbor_route)
    return neighbor_route

def update_temperature(temperature, cooling_rate):
    # print("New temperature: ", temperature * cooling_rate)
    return temperature * cooling_rate

# for testing states_per_temperature = 10, 50, 100, 500 for tiny, small, medium, large
# 500 takes too long
def simulated_annealing(
    initial_route,
    distance_matrix,
    initial_temperature,
    cooling_rate,
    stopping_temperature,
    max_iterations,
    random_type,
    states_per_temperature = 100
):

    current_route = initial_route.copy()

    current_distance = compute_route_distance(
        current_route,
        distance_matrix
    )

    best_route = current_route.copy()
    best_distance = current_distance

    temperature = initial_temperature

    iteration = 0

    history = [best_distance]

    while (temperature > stopping_temperature and iteration < max_iterations):
        # HUGE improvement!
        # Go back to the best route found so far after decrementing temperature!
        current_route = best_route.copy()
        # Generate a neighborhood (sets of neighbors)
        for _ in range(states_per_temperature):
            if random_type == "reverse":
                neighbor_route = generate_neighbor_by_reverse(current_route)
            else:
                neighbor_route = generate_neighbor_by_swapping(current_route)
                

            neighbor_distance = compute_route_distance(
                neighbor_route,
                distance_matrix
            )

            delta = neighbor_distance - current_distance

            # Always accept improvements
            if delta <= 0:

                current_route = neighbor_route
                current_distance = neighbor_distance

            # Randomly accept worse solutions
            else:

                probability = math.exp(-delta / temperature)

                alpha = random.random()

                if alpha <= probability:

                    current_route = neighbor_route
                    current_distance = neighbor_distance

            # check for best solution so far
            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance
                print("best_route: ", best_route)

            history.append(best_distance)

            iteration += 1

            if iteration >= max_iterations:
                break
            # print(
            #     "Temp:",
            #     temperature,
            #     "Current:",
            #     current_distance,
            #     "Neighbor:",
            #     neighbor_distance,
            #     "Delta:",
            #     delta,
            #     "Prob:",
            #     probability
            # )
        # Cool temperature to find new neighborhood
        temperature = update_temperature(
            temperature,
            cooling_rate
        )

    return best_route, best_distance, history