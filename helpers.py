import math

# ========================================== Distance Functions ==========================================

def get_distance(node1, node2, distance_type):

    x1, y1 = node1
    x2, y2 = node2

    if distance_type == "euclidean":
        return math.dist(node1, node2)

    return abs(x2 - x1) + abs(y2 - y1)

# ========================================== Route Evaluation ==========================================

def compute_route_distance(route, distance_matrix):

    total_distance = 0

    for i in range(len(route) - 1):

        current_city = route[i]
        next_city = route[i + 1]

        total_distance += distance_matrix[current_city][next_city]

    return total_distance