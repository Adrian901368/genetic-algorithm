from random import *
from copy import deepcopy
from math import *
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Define constants
MEMORY_SIZE = 64
POPULATION_SIZE = 200
MAX_STEPS = 500
NUM_OF_GENERATIONS = 3000 # Set the number of generations you want
STEPS_PENALTY = -1
TREASURE_BONUS = 15
OUT_OF_BOUNDS_PENALTY = -5
MUTATION_RATE = 0.1

class Dna:
    def __init__(self):
        self.memory = generate_random_dna()  # Initialize memory with random 8-bit binary numbers

    def increment(self, binary_number: str) -> str:
        num = int(binary_number, 2)
        incremented_num = (num + 1) % 256  # 1 byte wraps around at 256
        return format(incremented_num, '08b')

    def decrement(self, binary_number: str) -> str:
        num = int(binary_number, 2)
        decremented_num = (num - 1) % 256  # Wrap-around using modulo
        return format(decremented_num, '08b')

    def count_ones(self, binary_number: str) -> int:
        return binary_number.count('1')

    def binary_to_decimal(self, binary_number: str) -> int:
        return int(binary_number, 2)

    def print_memory(self):
        print("Memory Table:")
        for i in range(MEMORY_SIZE):
            print(f"Cell {i:02d}: {self.memory[i]}")

class Finder:
    def __init__(self, dna_sequence=None):
        self.table = Dna()
        if dna_sequence:
            self.set_dna(dna_sequence)
        self.original_dna = deepcopy(self.table.memory)
        self.movingsteps = 0
        self.fitness = 0
        self.log = []

    def set_dna(self, dna_sequence):
        if is_valid_dna(dna_sequence):
            self.table.memory = dna_sequence
        else:
            raise ValueError("DNA sequence must match MEMORY_SIZE and be valid.")

    def move_finder(self, max_steps=MAX_STEPS):
        # Initial settings
        pc = 0  # Program Counter
        steps = 0
        finder_position = (3,6)  # Starting position of the finder
        treasures = [(4, 5), (1, 4), (2, 2), (4, 1), (6, 3)]  # List of treasures
        found_treasures = set()
        treasure_found = [False] * len(treasures)  # Flag for each treasure
        out_of_bounds = False

        while steps < max_steps:
            # Check if the finder is out of bounds
            if not (0 <= finder_position[0] <= 6 and 0 <= finder_position[1] <= 6):
                out_of_bounds = True
                self.log.append(f"Finder out of bounds at {finder_position}")
                break

            # Check if all treasures are found
            if all(treasure_found):
                self.log.append("\n *** All treasures found! *** ")
                break

            position = pc % MEMORY_SIZE  # Ensure we stay within MEMORY_SIZE memory cells
            value = self.table.memory[position]  # Get the current instruction
            instruction = value[:2]  # First two bits determine the instruction type
            next_val_position = self.table.binary_to_decimal(value[2:])  # Next 6 bits represent the address
            next_value = self.table.memory[next_val_position]  # The value in the memory cell at that address

            if instruction == '00':  # Increment
                self.table.memory[next_val_position] = self.table.increment(next_value)
                pc += 1  # Move to the next instruction
            elif instruction == '01':  # Decrement
                self.table.memory[next_val_position] = self.table.decrement(next_value)
                pc += 1  # Move to the next instruction
            elif instruction == '10':  # Jump
                pc = self.table.binary_to_decimal(value[2:])  # Jump to the new address
            elif instruction == '11':  # Print
                ones_count = self.table.count_ones(next_value)
                if ones_count <= 2:
                    self.log.append("H")  # Move Up
                    finder_position = (finder_position[0], finder_position[1] - 1)
                    self.movingsteps += 1
                elif ones_count <= 4:
                    self.log.append("D")  # Move Down
                    finder_position = (finder_position[0], finder_position[1] + 1)
                    self.movingsteps += 1
                elif ones_count <= 6:
                    self.log.append("P")  # Move Right
                    finder_position = (finder_position[0] + 1, finder_position[1])
                    self.movingsteps += 1
                else:
                    self.log.append("L")  # Move Left
                    finder_position = (finder_position[0] - 1, finder_position[1])
                    self.movingsteps += 1

                # Check if the new position contains a treasure
                if finder_position in treasures:
                    treasure_index = treasures.index(finder_position)
                    if not treasure_found[treasure_index]:
                        found_treasures.add(finder_position)
                        treasure_found[treasure_index] = True  # Mark the treasure as found
                        #print("Treasure found", finder_position, end="")

                pc += 1  # Move to the next instruction

            steps += 1  # Count the step

        return finder_position, found_treasures, out_of_bounds, treasure_found

    def calculate_fitness(self, found_treasures, out_of_bounds, finder_position, treasures):
        # Initial fitness score
        self.fitness = 0

        # Deduct points for the number of steps taken
        self.fitness += STEPS_PENALTY * self.movingsteps

        # Add bonus points for each treasure found
        self.fitness += TREASURE_BONUS * (2 ** len(found_treasures))

        # Deduct points for being out of bounds
        if out_of_bounds:
            self.fitness += OUT_OF_BOUNDS_PENALTY

        # Penalty for missing treasures based on Manhattan distance
        missing_treasures = [treasure for i, treasure in enumerate(treasures) if not treasure_found[i]]
        for i, treasure in enumerate(missing_treasures):
            distance = calculate_distance(finder_position, treasure)
            # Apply penalty based on distance (more penalties for multiple missing treasures)
            self.fitness -= distance**(1/2) * (i + 1)

        return self.fitness

# Function to generate a random DNA sequence
def generate_random_dna():
    return [format(randint(0, 255), '08b') for _ in range(MEMORY_SIZE)]

# Function to check if DNA sequence is valid
def is_valid_dna(dna_sequence):
    return len(dna_sequence) == MEMORY_SIZE and all(len(code) == 8 for code in dna_sequence)

# Function to perform crossover between two DNA sequences
def two_point_crossover(dna1, dna2):
    point1 = randint(0, MEMORY_SIZE // 3)
    point2 = randint(2 * MEMORY_SIZE // 3, MEMORY_SIZE - 1)
    # Create children by crossing over between point1 and point2
    child1 = dna1[:point1] + dna2[point1:point2] + dna1[point2:]
    child2 = dna2[:point1] + dna1[point1:point2] + dna2[point2:]
    return child1, child2

# Function to perform mutation on a DNA sequence
def mutate(dna_sequence, mutation_rate=MUTATION_RATE):
    mutated_dna = []
    for gene in dna_sequence:
        if randint(0, 100) / 100.0 < mutation_rate:
            mutated_dna.append(format(randint(0, 255), '08b'))
        else:
            mutated_dna.append(gene)
    return mutated_dna

# Function to create the next generation with crossover and mutation

def calculate_distance(pos1, pos2):
    return int(fabs(pos1[0] - pos2[0]) + fabs(pos1[1] - pos2[1]))

def create_next_generation(previous_generation):
    # Sort finders by fitness
    previous_generation.sort(key=lambda f: f.fitness, reverse=True)

    next_generation = []

    # Randomly select the number of top parents (between 1 and 9)
    num_top_parents = randint(1, min(10, len(previous_generation) - 1))

    # Ensure there are enough remaining parents to sample from
    remaining_parents_count = len(previous_generation) - num_top_parents
    num_random_parents = min(POPULATION_SIZE - num_top_parents, remaining_parents_count)  # Subtract 2 for the top finders

    # Add the top 2 finders with their original DNA to the next generation
    for i in range(min(num_top_parents , len(previous_generation))):
        best_finder = previous_generation[i]
        best_dna = best_finder.original_dna
        #mutate(best_dna, 0.01)
        next_generation.append(Finder(dna_sequence=best_dna))

    # Select top N parents
    top_parents = previous_generation[:num_top_parents]

    # Select random parents
    random_parents = sample(previous_generation[num_top_parents:], num_random_parents)

    # Combine top parents and random
    parents = top_parents + random_parents

    # Create crossover and mutation to children
    for _ in range((POPULATION_SIZE - len(next_generation)) // 2):
        parent1, parent2 = sample(parents, 2)
        child_dna1, child_dna2 = two_point_crossover(parent1.table.memory, parent2.table.memory)
        child_dna1 = mutate(child_dna1)
        child_dna2 = mutate(child_dna2)

        if is_valid_dna(child_dna1):
            next_generation.append(Finder(dna_sequence=child_dna1))
        if is_valid_dna(child_dna2):
            next_generation.append(Finder(dna_sequence=child_dna2))

    return next_generation



# Create the first population of finders (each with its own DNA sequence)
finders = [Finder(dna_sequence=generate_random_dna()) for _ in range(POPULATION_SIZE)]
generations_fitness = [0]*NUM_OF_GENERATIONS
# Evolution loop
for generation in range(NUM_OF_GENERATIONS):
    print(f"\n-------------------------- Generation {generation + 1} ---------------")

    best_fitness = float('-inf')  # Initialize the best fitness with a very low value
    best_finder = None  # To store the best finder of the generation
    best_finder_position = None
    best_found_treasures = None

    for i, finder in enumerate(finders):
        # Pass the treasures as a result from move_finder
        finder_position, found_treasures, out_of_bounds, treasure_found = finder.move_finder(MAX_STEPS)
        treasures = [(4, 5), (1, 4), (2, 2), (4, 1), (6, 3)]  # Define treasures here in the main loop
        fitness = finder.calculate_fitness(found_treasures, out_of_bounds, finder_position, treasures)

        # Update if this finder has a better fitness score
        if fitness > best_fitness:
            best_fitness = fitness
            best_finder = finder
            best_finder_position = finder_position
            best_found_treasures = found_treasures

    # Store the best fitness for the generation
    generations_fitness[generation] = best_fitness

    # Print the best finder of the generation
    print(f"Best Finder (Generation {generation + 1}):")
    print(f"Position: {best_finder_position} / Treasures Found: {best_found_treasures} / Fitness Score: {best_fitness}")
    print(" ".join(best_finder.log))

    # Create the next generation
    finders = create_next_generation(finders)

print("Evolution complete.")

root = tk.Tk()
root.title("Fitness Graph")

# Create a matplotlib Figure
fig = Figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)

# Plot the data
ax.plot(range(1, NUM_OF_GENERATIONS + 1), generations_fitness, marker='o', color='b', linestyle='-', linewidth=2, markersize=5)
ax.set_title("Fitness over Generations")
ax.set_xlabel("Generation")
ax.set_ylabel("Total Fitness")
ax.grid(True)

# Create a FigureCanvasTkAgg widget to embed the plot in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a quit button
button_quit = ttk.Button(root, text="Quit", command=root.quit)
button_quit.pack(side=tk.BOTTOM)

# Start the Tkinter event loop
root.mainloop()
