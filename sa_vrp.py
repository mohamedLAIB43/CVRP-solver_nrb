import numpy as np
import math

class CVRPInstance:
    def __init__(self, distance_matrix, demands, vehicle_capacity):
        self.distance_matrix = distance_matrix
        self.demands = demands
        self.vehicle_capacity = vehicle_capacity
        self.num_customers = len(distance_matrix) - 1

class CVRPSolution:
    def __init__(self, instance, routes=None):
        self.instance = instance
        self.routes = routes if routes else [[] for _ in range(len(instance.vehicle_capacity))]
        self.calculate_fitness()

    def calculate_fitness(self):
        self.total_distance = sum(self.calculate_route_distance(route) for route in self.routes)

    def calculate_route_distance(self, route):
        if not route:
            return 0
        distance = self.instance.distance_matrix[0][route[0]]
        for i in range(len(route) - 1):
            distance += self.instance.distance_matrix[route[i]][route[i+1]]
        distance += self.instance.distance_matrix[route[-1]][0]
        return distance

    def swap(self, i, j):
        new_routes = [route.copy() for route in self.routes]
        new_routes[i], new_routes[j] = new_routes[j], new_routes[i]
        new_solution = CVRPSolution(self.instance, new_routes)
        return new_solution

class SA:
    def __init__(self, instance, initial_temperature, cooling_rate):
        self.instance = instance
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate

    def generate_initial_solution(self):
        initial_routes = [[] for _ in range(len(self.instance.vehicle_capacity))]
        customers = list(range(1, self.instance.num_customers + 1))
        for customer in customers:
            added = False
            for i, route in enumerate(initial_routes):
                if sum(self.instance.demands[node] for node in route) + self.instance.demands[customer] <= self.instance.vehicle_capacity[i]:
                    route.append(customer)
                    added = True
                    break
            if not added:
                initial_routes.append([customer])
        return CVRPSolution(self.instance, initial_routes)

    def acceptance_probability(self, old_distance, new_distance, temperature):
        if new_distance < old_distance:
            return 1.0
        return math.exp((old_distance - new_distance) / temperature)

    def solve(self, max_iterations):
        current_solution = self.generate_initial_solution()
        best_solution = current_solution
        temperature = self.initial_temperature
        for iteration in range(max_iterations):
            temperature *= 1 - self.cooling_rate
            for i in range(len(current_solution.routes)):
                for j in range(i + 1, len(current_solution.routes)):
                    new_solution = current_solution.swap(i, j)
                    new_solution.calculate_fitness()
                    delta_distance = new_solution.total_distance - current_solution.total_distance
                    if delta_distance < 0 or np.random.rand() < self.acceptance_probability(current_solution.total_distance, new_solution.total_distance, temperature):
                        current_solution = new_solution
                        if current_solution.total_distance < best_solution.total_distance:
                            best_solution = current_solution
        return best_solution

def main():
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    demands = [0, 10, 15, 30]
    vehicle_capacity = [50, 50]

    instance = CVRPInstance(distance_matrix, demands, vehicle_capacity)
    sa = SA(instance, initial_temperature=1000, cooling_rate=0.003)
    solution = sa.solve(max_iterations=1000)

    print("Routes:")
    for i, route in enumerate(solution.routes):
        print(f"Vehicle {i}: {route}, Distance: {solution.calculate_route_distance(route)}")
    print(f"Total distance traveled: {solution.total_distance}")

if __name__ == '__main__':
    main()
