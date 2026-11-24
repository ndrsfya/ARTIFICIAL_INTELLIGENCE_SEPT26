"""
ARTIFICIAL INTELLIGENCE ASSIGNMENT
Genetic Algorithm for Delivery Route Optimisation

Dataset:
    The fictional delivery-distance matrix supplied in the assignment.
    This program does NOT use the Lab 8 medical insurance dataset.

Submission:
    - Save this file as ga_delivery_route.py.
    - Run it to find a short route from depot A through B-G and back to A.
    - The program also saves the console result as GA_console_output.txt.

Genetic Algorithm settings:
    Population size : 100
    Generations     : 200 (minimum required: 50)
    Random seed     : 42
    Mutation rate   : 0.20
    Elite routes    : 2
"""

import random
from pathlib import Path

# ------------------------------------------------------------
# 1. Assignment distance matrix (kilometres)
# Row and column order: A, B, C, D, E, F, G
# ------------------------------------------------------------

distance_matrix = [
    [0, 4, 8, 6, 7, 9, 5],
    [4, 0, 5, 7, 3, 8, 6],
    [8, 5, 0, 4, 6, 3, 7],
    [6, 7, 4, 0, 5, 6, 8],
    [7, 3, 6, 5, 0, 4, 6],
    [9, 8, 3, 6, 4, 0, 5],
    [5, 6, 7, 8, 6, 5, 0]
]

depot = "A"
delivery_locations = ["B", "C", "D", "E", "F", "G"]

# Convert each location name to its corresponding matrix index.
location_indexes = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6
}


# ------------------------------------------------------------
# 2. Calculate the complete route distance
# Include the trip from depot A and the return to depot A.
# ------------------------------------------------------------

def calculate_route_distance(route):
    complete_route = [depot] + route + [depot]
    total_distance = 0

    for position in range(len(complete_route) - 1):
        current_location = location_indexes[complete_route[position]]
        next_location = location_indexes[complete_route[position + 1]]

        total_distance += distance_matrix[current_location][next_location]

    return total_distance


# ------------------------------------------------------------
# 3. Create the initial population
# Each chromosome is a shuffled list of B-G.
# Therefore, every initial route is valid.
# ------------------------------------------------------------

def create_initial_population(population_size):
    population = []

    for _ in range(population_size):
        route = delivery_locations.copy()
        random.shuffle(route)
        population.append(route)

    return population


# ------------------------------------------------------------
# 4. Parent selection using tournament selection
# Randomly choose three routes and select the shortest one.
# ------------------------------------------------------------

def select_parent(population):
    candidates = random.sample(population, 3)
    best_candidate = min(candidates, key=calculate_route_distance)

    return best_candidate


# ------------------------------------------------------------
# 5. Route-preserving crossover (Order Crossover)
# Copy a section from parent 1, then fill empty positions
# using the order of locations in parent 2.
# This prevents repeated or missing locations.
# ------------------------------------------------------------

def order_crossover(parent_one, parent_two):
    route_length = len(parent_one)

    first_position, last_position = sorted(
        random.sample(range(route_length), 2)
    )

    child = [None] * route_length

    # Copy a section from the first parent.
    child[first_position:last_position + 1] = (
        parent_one[first_position:last_position + 1]
    )

    # Get locations from the second parent that are not already copied.
    remaining_locations = [
        location for location in parent_two
        if location not in child
    ]

    # Fill the empty positions with the remaining locations.
    empty_positions = [
        position for position in range(route_length)
        if child[position] is None
    ]

    for position, location in zip(empty_positions, remaining_locations):
        child[position] = location

    return child


# ------------------------------------------------------------
# 6. Mutation using swap mutation
# With the selected mutation probability, swap two locations.
# The route remains valid because no location is added or removed.
# ------------------------------------------------------------

def mutate_route(route, mutation_rate):
    mutated_route = route.copy()

    if random.random() < mutation_rate:
        first_position, second_position = random.sample(
            range(len(mutated_route)), 2
        )

        mutated_route[first_position], mutated_route[second_position] = (
            mutated_route[second_position],
            mutated_route[first_position]
        )

    return mutated_route


# ------------------------------------------------------------
# 7. Run the Genetic Algorithm
# Elitism copies the best routes unchanged into each generation.
# ------------------------------------------------------------

def run_genetic_algorithm(
    random_seed=42,
    population_size=100,
    number_of_generations=200,
    mutation_rate=0.20,
    number_of_elites=2
):
    # Fixed seed makes the experiment reproducible.
    random.seed(random_seed)

    population = create_initial_population(population_size)

    best_route = min(
        population,
        key=calculate_route_distance
    ).copy()

    for generation in range(number_of_generations):

        # Sort routes from shortest to longest.
        population.sort(key=calculate_route_distance)

        # Update the best route found so far.
        if calculate_route_distance(population[0]) < calculate_route_distance(best_route):
            best_route = population[0].copy()

        # Elitism: preserve the best routes unchanged.
        next_generation = [
            route.copy()
            for route in population[:number_of_elites]
        ]

        # Create new children until the population is full.
        while len(next_generation) < population_size:
            parent_one = select_parent(population)
            parent_two = select_parent(population)

            child = order_crossover(parent_one, parent_two)
            child = mutate_route(child, mutation_rate)

            next_generation.append(child)

        population = next_generation

    # Check the final generation for a better route.
    final_best_route = min(
        population,
        key=calculate_route_distance
    )

    if calculate_route_distance(final_best_route) < calculate_route_distance(best_route):
        best_route = final_best_route.copy()

    best_distance = calculate_route_distance(best_route)

    return best_route, best_distance


# ------------------------------------------------------------
# 8. Main program
# Print the best route and save a copy of the console output.
# ------------------------------------------------------------

def main():
    random_seed = 42
    population_size = 100
    number_of_generations = 200
    mutation_rate = 0.20
    number_of_elites = 2

    best_route, best_distance = run_genetic_algorithm(
        random_seed=random_seed,
        population_size=population_size,
        number_of_generations=number_of_generations,
        mutation_rate=mutation_rate,
        number_of_elites=number_of_elites
    )

    complete_route = [depot] + best_route + [depot]

    output_lines = [
        "GENETIC ALGORITHM - DELIVERY ROUTE OPTIMISATION",
        "Dataset: Fictional assignment distance matrix",
        f"Random seed: {random_seed}",
        f"Population size: {population_size}",
        f"Number of generations: {number_of_generations}",
        f"Mutation rate: {mutation_rate}",
        f"Number of elite routes: {number_of_elites}",
        "",
        "Best route:",
        " -> ".join(complete_route),
        "",
        f"Total distance: {best_distance} km"
    ]

    output_text = "\n".join(output_lines)

    # Display the result in the terminal.
    print(output_text)

    # Save the same output as evidence for the assignment.
    output_file = Path(__file__).resolve().parent / "GA_console_output.txt"
    output_file.write_text(output_text + "\n", encoding="utf-8")

    print(f"\nConsole output saved to: {output_file}")


if __name__ == "__main__":
    main()
