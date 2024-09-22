from random import randint, sample
from copy import deepcopy

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Define constants
MEMORY_SIZE = 64
POPULATION_SIZE = 20
MAX_STEPS = 500
NUM_OF_GENERATIONS = 300  # Set the number of generations you want
STEPS_PENALTY = -0.5
TREASURE_BONUS = 20
OUT_OF_BOUNDS_PENALTY = -5
MUTATION_RATE = 0.01

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
        self.movingsteps = 0
        self.fitness = 0

    def set_dna(self, dna_sequence):
        """Sets the DNA of the finder."""
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
                print("Finder out of bounds at", finder_position, end=" ")
                break

            # Check if all treasures are found
            if all(treasure_found):
                print("All treasures found!")
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
                    print("H", end=" ")  # Move Up
                    finder_position = (finder_position[0], finder_position[1] - 1)
                    self.movingsteps += 1
                elif ones_count <= 4:
                    print("D", end=" ")  # Move Down
                    finder_position = (finder_position[0], finder_position[1] + 1)
                    self.movingsteps += 1
                elif ones_count <= 6:
                    print("P", end=" ")  # Move Right
                    finder_position = (finder_position[0] + 1, finder_position[1])
                    self.movingsteps += 1
                else:
                    print("L", end=" ")  # Move Left
                    finder_position = (finder_position[0] - 1, finder_position[1])
                    self.movingsteps += 1

                # Check if the new position contains a treasure
                if finder_position in treasures:
                    treasure_index = treasures.index(finder_position)
                    if not treasure_found[treasure_index]:
                        found_treasures.add(finder_position)
                        treasure_found[treasure_index] = True  # Mark the treasure as found
                        print("Treasure found", finder_position, end="")

                pc += 1  # Move to the next instruction

            steps += 1  # Count the step

        return finder_position, found_treasures, out_of_bounds

    def calculate_fitness(self, found_treasures, out_of_bounds):
        # Calculate score
        self.fitness = 0
        # Deduct points for steps taken
        self.fitness += STEPS_PENALTY * self.movingsteps
        # Add points for each treasure found
        self.fitness += (len(found_treasures) * (TREASURE_BONUS + 20*len(found_treasures)))
        # Deduct points for being out of bounds
        if out_of_bounds:
            self.fitness += OUT_OF_BOUNDS_PENALTY

        return self.fitness

# Function to generate a random DNA sequence
def generate_random_dna():
    """Generates a random DNA sequence."""
    return [format(randint(0, 255), '08b') for _ in range(MEMORY_SIZE)]

# Function to check if DNA sequence is valid
def is_valid_dna(dna_sequence):
    """Checks if the DNA sequence is valid."""
    return len(dna_sequence) == MEMORY_SIZE and all(len(code) == 8 for code in dna_sequence)

# Function to perform crossover between two DNA sequences
def two_point_crossover(dna1, dna2):
    """Perform two-point crossover between two DNA sequences."""
    point = randint(0, MEMORY_SIZE - 1)
    point2 = randint(0, MEMORY_SIZE - 1)  # Ensure point2 > point1

    # Create new DNA sequences by swapping segments between the two points
    child1 = dna1[:point] + dna2[point:]
    child2 = dna2[:point2] + dna1[point2:]

    return child1, child2

# Function to perform mutation on a DNA sequence
def mutate(dna_sequence, mutation_rate=MUTATION_RATE):
    """Perform mutation on a DNA sequence."""
    mutated_dna = []
    for gene in dna_sequence:
        if randint(0, 100) / 100.0 < mutation_rate:
            mutated_dna.append(format(randint(0, 255), '08b'))
        else:
            mutated_dna.append(gene)
    return mutated_dna

# Function to create the next generation with crossover and mutation
from random import sample, choice

def create_next_generation(previous_generation):
    # Flatten the list of finders
    flat_previous_generation = [finder for finder in previous_generation]

    # Sort finders by fitness
    flat_previous_generation.sort(key=lambda f: f.fitness, reverse=True)

    next_generation = []

    # Select the top 5 finders
    top_five = flat_previous_generation[:5]

    # Randomly choose 5 more from the rest of the population
    random_five = sample(flat_previous_generation[5:], 5)

    # Combine the selected parents
    parents = top_five + random_five

    # Add the top 5 directly to the next generation
    for parent in top_five:
        next_generation.append(parent)

    # Create offspring through crossover and mutation
    for _ in range((POPULATION_SIZE - len(top_five)) // 2):
        parent1, parent2 = sample(parents, 2)
        child_dna1, child_dna2 = two_point_crossover(parent1.table.memory, parent2.table.memory)
        child_dna1 = mutate(child_dna1)
        child_dna2 = mutate(child_dna2)

        # Validate the DNA and add to the next generation
        if is_valid_dna(child_dna1):
            next_generation.append(Finder(dna_sequence=child_dna1))
        else:
            next_generation.append(Finder(dna_sequence=generate_random_dna()))

        if is_valid_dna(child_dna2):
            next_generation.append(Finder(dna_sequence=child_dna2))
        else:
            next_generation.append(Finder(dna_sequence=generate_random_dna()))

    return next_generation


# Create the first population of finders (each with its own DNA sequence)
finders = [Finder(dna_sequence=generate_random_dna()) for _ in range(POPULATION_SIZE)]
generations_fitness = [0]*NUM_OF_GENERATIONS
# Evolution loop
for generation in range(NUM_OF_GENERATIONS):
    print(f"\n-------------------------- Generation {generation + 1} ---------------")

    for i, finder in enumerate(finders):
        print(f"Finder {i + 1} (Generation {generation + 1}):")
        finder_position, found_treasures, out_of_bounds = finder.move_finder(MAX_STEPS)
        fitness = finder.calculate_fitness(found_treasures, out_of_bounds)
        generations_fitness[generation] += fitness
        print(f"Position: {finder_position} / Treasures Found: {found_treasures} / Fitness Score: {fitness}")

    # Create next generation
    print(f"fitness total - {generations_fitness[generation]}")
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
