import matplotlib.pyplot as plt
import os
import pandas as pd


# ==========================================
# Convergence Plot
# ==========================================

def plot_convergence(history, output_file="convergence.png"):
    """
    Plot best distance over iterations.

    INPUT:
        history:
            List of best distances over time.

        output_file:
            Filename for saved plot.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(history)

    plt.xlabel("Iteration")
    plt.ylabel("Best Distance")
    plt.title("Simulated Annealing Convergence")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(output_file)

    # plt.show()

    # plt.close()

    print(f"Saved convergence plot to: {output_file}")


# ==========================================
# Route Visualization
# ==========================================

def plot_route(
    route,
    cities,
    title="TSP Route",
    output_file="route.png"
):
    """
    Plot a TSP route.

    INPUT:
        route:
            Route list.
            Example:
                [0, 4, 2, 5, 1]

        cities:
            Original city data structure:
                [(index, (x, y)), ...]

        title:
            Plot title.

        output_file:
            Filename for saved image.
    """

    # Build lookup table
    city_lookup = dict(cities)

    # Extract coordinates in route order
    x_coords = []
    y_coords = []

    for city_index in route:

        x, y = city_lookup[city_index]

        x_coords.append(x)
        y_coords.append(y)

    # Return to start city
    start_x, start_y = city_lookup[route[0]]

    x_coords.append(start_x)
    y_coords.append(start_y)

    plt.figure(figsize=(8, 8))

    # Plot route
    plt.plot(x_coords, y_coords, marker='o')

    # Label cities
    for city_index in route:

        x, y = city_lookup[city_index]

        plt.text(x, y, str(city_index))

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")

    plt.title(title)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(output_file)

    # plt.show()

    # plt.close()

    print(f"Saved route visualization to: {output_file}")


# ==========================================
# Side-by-Side Route Comparison
# ==========================================

def plot_route_comparison(
    initial_route,
    final_route,
    cities,
    output_file="route_comparison.png"
):
    """
    Plot initial and final routes side-by-side.
    """

    city_lookup = dict(cities)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    routes = [
        (initial_route, "Initial Route"),
        (final_route, "Final Route")
    ]

    for ax, (route, title) in zip(axes, routes):

        x_coords = []
        y_coords = []

        for city_index in route:

            x, y = city_lookup[city_index]

            x_coords.append(x)
            y_coords.append(y)

        # Return to start
        start_x, start_y = city_lookup[route[0]]

        x_coords.append(start_x)
        y_coords.append(start_y)

        ax.plot(x_coords, y_coords, marker='o')

        for city_index in route:

            x, y = city_lookup[city_index]

            ax.text(x, y, str(city_index))

        ax.set_title(title)

        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")

        ax.grid(True)

    plt.tight_layout()

    plt.savefig(output_file)

    # plt.show()

    # plt.close()

    print(f"Saved comparison plot to: {output_file}")