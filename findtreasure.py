from random import randint

# Define constants
MEMORY_SIZE = 64
POPULATION_SIZE = 20
MAX_STEPS = 500
STEPS_PENALTY = -1
TREASURE_BONUS = 20
OUT_OF_BOUNDS_PENALTY = -20

class Table:
    def __init__(self):
        self.memory = [format(randint(0, 255), '08b') for _ in range(MEMORY_SIZE)]  # Initialize memory with random 8-bit binary numbers

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
        self.table = Table()
        self.movingsteps = 0
        self.fitness = 20

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

    def calculate_fitness(self,finder_position, found_treasures, out_of_bounds):
        # Calculate score

        # Deduct points for steps taken
        self.fitness += STEPS_PENALTY * self.movingsteps
        # Add points for each treasure found
        self.fitness += (len(found_treasures) * TREASURE_BONUS)
        # Deduct points for being out of bounds
        if out_of_bounds:
            self.fitness += OUT_OF_BOUNDS_PENALTY

        return self.fitness

# Create a population of finders (each with its own memory table)
population = [Finder() for _ in range(POPULATION_SIZE)]

# Run the move_finder function for each finder and print the results along with fitness
for i, finder in enumerate(population):
    print(f"Finder {i + 1}:")
    finder_position, found_treasures, out_of_bounds = finder.move_finder(MAX_STEPS)
    fitness = finder.calculate_fitness(finder_position, found_treasures, out_of_bounds)
    print(f"Fpos: {finder_position} / Treasures: {found_treasures} / Fitness Score: {fitness}")
    print()
