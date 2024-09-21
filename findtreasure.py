from random import randint

def increment(binary_number: str) -> str:
    num = int(binary_number, 2)
    incremented_num = (num + 1) % 256
    return format(incremented_num, '08b')

def decrement(binary_number: str) -> str:
    num = int(binary_number, 2)
    decremented_num = (num - 1) % 256
    return format(decremented_num, '08b')

def count_ones(binary_number: str) -> int:
    return binary_number.count('1')

def binary_to_decimal(binary_number: str) -> int:
    return int(binary_number, 2)

instruction_table = []
for i in range(64):
    binary_number = format(randint(0, 255), '08b')
    instruction_table.append(binary_number)

steps = 0
ix_adress = 0

while steps < 100:
    position = ix_adress % 64
    value = instruction_table[position]
    instruction = value[:2]
    next_val_position = binary_to_decimal(value[2:])
    next_value = instruction_table[next_val_position]

    if instruction == '00':  # Increment
        instruction_table[next_val_position] = increment(next_value)
        ix_adress += 1
    elif instruction == '01':  # Decrement
        instruction_table[next_val_position] = decrement(next_value)
        ix_adress += 1
    elif instruction == '10':  # Jump
        ix_adress = binary_to_decimal(value[2:])
    else:  # Print
        if count_ones(next_value) <= 2:
            print("H", end=" ")
        elif count_ones(next_value) <= 4:
            print("D", end=" ")
        elif count_ones(next_value) <= 6:
            print("P", end=" ")
        else:
            print("L", end=" ")
        ix_adress += 1
    steps += 1
