from random import randint
from copy import deepcopy

# Define constants
MEMORY_SIZE = 64
POPULATION_SIZE = 6
MAX_STEPS = 500
NUM_OF_GENERATIONS = 4  # Set the number of generations you want
STEPS_PENALTY = -1
TREASURE_BONUS = 20
OUT_OF_BOUNDS_PENALTY = -20


class Dna:
    def __init__(self):
        self.memory = [format(randint(0, 255), '08b') for _ in
                       range(MEMORY_SIZE)]  # Initialize memory with random 8-bit binary numbers

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
    def __init__(self):
        self.table = Dna()
        self.movingsteps = 0
        self.fitness = 0

    def move_finder(self, max_steps=MAX_STEPS):
        # Initial settings
        pc = 0  # Program Counter
        steps = 0
        finder_position = (3, 6)  # Starting position of the finder
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

    def calculate_fitness(self, finder_position, found_treasures, out_of_bounds):
        # Calculate score

        # Deduct points for steps taken
        self.fitness += STEPS_PENALTY * self.movingsteps
        # Add points for each treasure found
        self.fitness += (len(found_treasures) * TREASURE_BONUS)
        # Deduct points for being out of bounds
        if out_of_bounds:
            self.fitness += OUT_OF_BOUNDS_PENALTY

        return self.fitness


def evaluate_and_sort_population(population):
    for finder in population:
        # Run the Finder's movement logic
        finder_position, found_treasures, out_of_bounds = finder.move_finder(MAX_STEPS)

        # Calculate fitness for the Finder
        finder.fitness = finder.calculate_fitness(finder_position, found_treasures, out_of_bounds)

    # Sort the population by fitness (descending order)
    population.sort(key=lambda f: f.fitness, reverse=True)
    return population







# Function to create the next generation by copying the previous one
def create_next_generation(previous_generation):
    # Create a new population with identical DNA as the previous generation
    next_generation = [deepcopy(finder) for finder in previous_generation]
    return next_generation


# Create the first population of finders (each with its own memory table)
generation_1 = [Finder() for _ in range(POPULATION_SIZE)]

# This will hold multiple generations
generations = []

# Add the first generation (which is your current population)
generations.append(generation_1)

# Create the next generations as copies of the previous generation
for gen_num in range(1, NUM_OF_GENERATIONS):
    next_generation = create_next_generation(generations[gen_num - 1])
    generations.append(next_generation)

# Now, you have `NUM_OF_GENS` generations in the `generations` list

# Outer loop for iterating over each generation
for generation_index, generation in enumerate(generations):
    print(f"\n-------------------------- Generation {generation_index + 1} -------------------------------")

    # Inner loop for iterating over each Finder in the current generation
    for finder_index, finder in enumerate(generation):
        print(f"Finder {finder_index + 1} (Generation {generation_index + 1}):")

        # Run the Finder's movement logic
        finder_position, found_treasures, out_of_bounds = finder.move_finder(MAX_STEPS)

        # Calculate fitness for the Finder
        fitness = finder.calculate_fitness(finder_position, found_treasures, out_of_bounds)

        # Print the Finder's status
        print(f"Fpos: {finder_position} / Treasures: {found_treasures} / Fitness Score: {fitness}")
        print()
