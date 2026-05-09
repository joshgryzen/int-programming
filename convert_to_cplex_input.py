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
    "-o",
    "--output",
    default="tsp_data.dat",
    type=str,
    help="Output .dat filename for CPLEX/OPL",
)

parser.add_argument(
    "-d",
    "--distance_type",
    choices=["euclidean", "manhattan"],
    default="euclidean",
    help="Distance metric",
)

args = parser.parse_args()

input_file = args.input
output_file = args.output
distance_type = args.distance_type

# ========================================== Load Cities ==========================================

df = pd.read_csv(input_file, names=["x", "y"])

cities = [(index, tuple(row)) for index, row in df.iterrows()]

n = len(cities)

# ========================================== Distance Function ==========================================

def get_distance(node1, node2):

    x1, y1 = node1
    x2, y2 = node2

    if distance_type == "euclidean":
        return round(math.dist(node1, node2), 4)

    return abs(x2 - x1) + abs(y2 - y1)

# ========================================== Build Distance Matrix ==========================================

distance_matrix = []

for i, position1 in cities:

    row = []

    for j, position2 in cities:

        distance = get_distance(position1, position2)

        row.append(distance)

    distance_matrix.append(row)

# ========================================== Write OPL .dat File ==========================================

with open(output_file, "w") as f:

    # Number of cities
    f.write(f"n = {n};\n\n")

    # Distance matrix
    f.write("dist = [\n")

    for row_index, row in enumerate(distance_matrix):

        formatted_row = ", ".join(map(str, row))

        if row_index < n - 1:
            f.write(f"  [{formatted_row}],\n")
        else:
            f.write(f"  [{formatted_row}]\n")

    f.write("];\n")

print(f"CPLEX data file written to: {output_file}")