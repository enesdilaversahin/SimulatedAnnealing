import numpy as np
import matplotlib.pyplot as plt
import logging
from datetime import datetime
from tqdm import tqdm  # Add tqdm library for progress bar

# Green color codes
GREEN = '\033[92m'
RESET = '\033[0m'

# Logger configuration
logging.basicConfig(filename='applog.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('my_logger')

def print_green(message):
    print(f"{GREEN}{message}{RESET}")

def input_green(prompt):
    return input(f"{GREEN}{prompt}{RESET}")
try:
    print_green("--------------------------------------------------")
    print_green("Simulated Annealing for Traveling Salesman Problem")
    print_green("----------Created by [enesdilaversahin]----------")
    print_green("")
    # Get parameters from user
    num_cities = int(input_green("Enter the number of cities: "))
    initial_temperature = float(input_green("Enter the initial temperature: "))
    cooling_rate = float(input_green("Enter the cooling rate (should be between 0 and 1): "))
    stopping_temperature = 1e-3

    # Function to generate cities
    def generate_cities(number):
        return np.random.rand(number, 2) * 100

    # Simulated annealing algorithm
    def simulated_annealing(cities, initial_temperature, cooling_rate, stopping_temperature):
        n = len(cities)
        best_tour = list(range(n))
        np.random.shuffle(best_tour)
        best_distance = float('inf')
        distances = []

        temperature = initial_temperature
        iteration = 0

        # Create a progress bar with 'tqdm'
        with tqdm(total=10000, desc=f"{GREEN}Simulation Progress{RESET}") as pbar:
            while temperature > stopping_temperature:
                for _ in range(100):
                    # Randomly select two cities
                    a, b = np.random.randint(0, n, 2)
                    new_tour = best_tour[:]
                    new_tour[a], new_tour[b] = new_tour[b], new_tour[a]
                    
                    # Calculate distance (modify according to your distance calculation method)
                    old_distance = sum(distance(cities[best_tour[i]], cities[best_tour[i - 1]]) for i in range(n))
                    new_distance = sum(distance(cities[new_tour[i]], cities[new_tour[i - 1]]) for i in range(n))
                    
                    if new_distance < best_distance or np.random.rand() < np.exp((old_distance - new_distance) / temperature):
                        best_tour = new_tour
                        best_distance = new_distance
                    
                    distances.append(best_distance)
                    
                temperature *= cooling_rate
                iteration += 1
                pbar.update(100)  # Update the progress bar every iteration
        
        return best_tour, best_distance, distances

    # Function to calculate distance between two cities
    def distance(city1, city2):
        return np.linalg.norm(city1 - city2)

    # Generate cities
    cities = generate_cities(num_cities)

    # Progress message
    print_green("Simulation is starting. Please wait...")
    logger.info("Simulation is starting. Please wait...")

    # Run simulated annealing algorithm
    best_tour, best_distance, distances = simulated_annealing(cities, initial_temperature, cooling_rate, stopping_temperature)

    # Get current date and time
    simulation_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Plot results
    plt.figure(figsize=(15, 7))

    # Show cities and the best tour
    plt.subplot(1, 2, 1)
    plt.scatter(cities[:, 0], cities[:, 1], c='red')
    tour_cities = np.array([cities[i] for i in best_tour + [best_tour[0]]])
    plt.plot(tour_cities[:, 0], tour_cities[:, 1], 'b-')
    plt.title('Best Tour')

    # Show distance changes
    plt.subplot(1, 2, 2)
    plt.plot(distances)
    plt.title('Tour Distance Changes')
    plt.xlabel('Iteration')
    plt.ylabel('Distance')

    # Save log information
    logger.info(f"Best distance for this tour: {best_distance}")

    # Save plot
    plt.tight_layout()
    plt.savefig(f'results_{simulation_time}.png')  # Create a filename with date and time
    plt.show()

    # Inform the user that the process is complete
    print_green(f"Simulation completed. Results saved to 'results_{simulation_time}.png'.")
    logger.info(f"Simulation completed. Results saved to 'results_{simulation_time}.png'.")

except Exception as e:
    logger.error("An error occurred: " + str(e))
    print_green("An error occurred. Check the log file for details.")
