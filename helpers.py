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

    for i in range(len(route)):

        current_city = route[i]

        next_city = route[
            (i + 1) % len(route)
        ]

        total_distance += (
            distance_matrix[current_city][next_city]
        )

    return total_distance

def compute_freezing_temperature(
    best_distance,
    neighbor_distance,
    v
):
    """
    Estimate freezing temperature using:

        Tf = (Em' - Em) / ln(v)
    """

    delta = neighbor_distance - best_distance

    # avoid divide-by-zero / invalid logs
    if v <= 1:
        v = 2

    # avoid negative temperatures
    if delta <= 0:
        delta = 0.0001

    return delta / math.log(v)