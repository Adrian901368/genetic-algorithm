Introduction
In this work, I implemented a simulation that uses a genetic algorithm to optimize treasure hunters in a grid. The goal is for the hunters to find all treasures in the shortest possible time, while optimizing their DNA through selection, crossover, and mutation.
Macros
At the beginning of the code, I set several macros that simplify the work and configuration of the program:

MEMORY_SIZE: Number of memory cells for DNA (64).
POPULATION_SIZE: Number of hunters in the population (e.g., 200).
MAX_STEPS: Maximum number of steps a hunter can take (500).
NUM_OF_GENERATIONS: Number of generations (e.g., 15,000).
MUTATION_RATE: Probability of mutation (e.g., 10%).
Additional constants include bonuses for found treasures, penalties for steps, and excursions outside the grid.

DNA Class
This class contains functions related to memory, where machine data is stored:

increment() and decrement(): Incrementation and decrementation of 8-bit numbers using a wrap-around mechanism (modulo 256).
binary_to_decimal(): Converting binary numbers to decimal, necessary for determining positions.
print_memory(): Displaying memory cells (DNA) of the hunter.

Finder Class
The Finder class is used to represent a hunter who performs the simulation:

table: An instance of the DNA class that stores the machine's memory.
original_dna: A copy of the original DNA, to be preserved even after modification during simulation.
fitness: Variable for storing the calculation of the fitness function.
log: Record of steps, including information about found treasures or excursions outside the grid.

Main functions in the class:

move_finder(): Simulates the movement of the hunter in the grid based on DNA.
calculate_fitness(): Calculates fitness based on the number of treasures found, number of steps, excursions outside the grid, and distances from unfound treasures. The formula for calculating fitness is: Bonus for found treasure * (2^number of treasures found) - (number of steps + excursion outside the grid + distance from unfound treasures)

Evolutionary Algorithm
I used a genetic algorithm that works as follows:

Initialization: For the first generation, each hunter is assigned a random sequence of 8-bit numbers in a 64-cell field (DNA).
Parent Selection: Based on the fitness function, individuals are sorted. The best individuals are selected using elitism and random selection.
Crossover: Two-point crossover is used, where the parents' DNA is divided into three parts and two offspring are created from combinations of these parts.
Mutation: Each gene has a certain probability of mutation (e.g., 10%), where it is randomly changed to a new 8-bit number.
DNA Validation: At the end, it is checked whether each hunter has valid DNA with the correct length and format.

Treasure Field
Treasures are placed in the grid at fixed positions. The hunter's movement is tracked, and when a treasure is found, its fitness increases. If the hunter goes outside the grid, it is penalized.
Simulation Termination Conditions:

The hunter finds all treasures, or
The hunter exceeds the maximum number of steps or leaves the grid.

Results and Optimization
During the development of the algorithm, I experimented with different types of selection and crossover:

Simple Selection: Initially, I selected only one best parent, which did not lead to optimal results.
Elitism Selection + Random (Addition) Selection: At the beginning, I selected a random number of the best parents from 1 to half the population (their DNA is retained from the previous generation) to which a remaining number of random individuals is added so that the number of parents is half of the population.
Single-point Crossover: Initially, simple single-point crossover was used, where the gene was split in half, which limited the variability of offspring.
Two-point Crossover: This type of crossover, along with random parent selection, which divides the gene (according to 2 random points) into 3 parts, brought the best results, so I kept it as the final solution.

Evaluation of Results

Greater variability in the population and more generations improved the success rate in finding all treasures.
Fitness around 100 meant finding 3 treasures, fitness around 200 finding 4, and fitness around 400 meant finding all 5 treasures.
Mutation had very little impact on results, whether it was set to 1%, 10%, or 30%.
