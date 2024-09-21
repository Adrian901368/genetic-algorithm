from random import randint

class Table:
    def __init__(self):
        self.memory = [format(randint(0, 255), '08b') for _ in range(64)]  # Initialize memory with random 8-bit binary numbers

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
        for i in range(64):
            print(f"Cell {i:02d}: {self.memory[i]}")




def move_finder(table, max_steps=100):
    # Initial settings
    pc = 0  # Program Counter
    steps = 0
    finder_position = (3, 6)  # Starting position of the finder
    treasures = [(4, 5), (1, 4), (2, 2), (4, 1), (6, 3)]  # List of treasures
    found_treasures = set()

    while steps < max_steps:
        # Check if the finder is out of bounds
        if not (0 <= finder_position[0] <= 6 and 0 <= finder_position[1] <= 6):
            print(" - Finder out of bounds!", end=" ")
            break

        # Check if all treasures are found
        if len(found_treasures) == len(treasures):
            print(" - All treasures found!", end=" ")
            break

        position = pc % 64  # Ensure we stay within 64 memory cells
        value = table.memory[position]  # Get the current instruction
        instruction = value[:2]  # First two bits determine the instruction type
        next_val_position = table.binary_to_decimal(value[2:])  # Next 6 bits represent the address
        next_value = table.memory[next_val_position]  # The value in the memory cell at that address

        if instruction == '00':  # Increment
            table.memory[next_val_position] = table.increment(next_value)
            pc += 1  # Move to the next instruction
        elif instruction == '01':  # Decrement
            table.memory[next_val_position] = table.decrement(next_value)
            pc += 1  # Move to the next instruction
        elif instruction == '10':  # Jump
            pc = table.binary_to_decimal(value[2:])  # Jump to the new address
        elif instruction == '11':  # Print
            ones_count = table.count_ones(next_value)
            if ones_count <= 2:
                print("H", end=" ")  # Move Up
                finder_position = (finder_position[0], finder_position[1] - 1)
            elif ones_count <= 4:
                print("D", end=" ")  # Move Down
                finder_position = (finder_position[0], finder_position[1] + 1)
            elif ones_count <= 6:
                print("P", end=" ")  # Move Right
                finder_position = (finder_position[0] + 1, finder_position[1])
            else:
                print("L", end=" ")  # Move Left
                finder_position = (finder_position[0] - 1, finder_position[1])

            # Update the finder position based on the move

            # Check if the new position contains a treasure
            if finder_position in treasures:
                found_treasures.add(finder_position)
                #print(f"Treasure found at {finder_position}!")

            pc += 1  # Move to the next instruction

        steps += 1  # Count the step

    print(f"Fpos:{finder_position}/Trsurs:{found_treasures}")

# Create an instance of Table and run the move_finder function
table = Table()
#table.print_memory()

# Run the move_finder function with a maximum of 100 steps
move_finder(table, 100)

#table.print_memory()
