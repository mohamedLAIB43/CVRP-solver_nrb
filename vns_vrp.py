import numpy as np

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

class VNS:
    def __init__(self, instance):
        self.instance = instance

    def generate_initial_solution(self):
        initial_routes = [[] for _ in range(len(self.instance.vehicle_capacity))]
        customers = list(range(1, self.instance.num_customers + 1))
        np.random.shuffle(customers)
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

    def local_search(self, solution):
        k_opt = 1
        improved = True
        while improved:
            improved = False
            for i in range(len(solution.routes)):
                for j in range(i + 1, len(solution.routes)):
                    new_solution = solution.swap(i, j)
                    if new_solution.total_distance < solution.total_distance:
                        solution = new_solution
                        improved = True
                        k_opt = 1
                        break
                if improved:
                    break
            k_opt += 1
        return solution

    def shake(self, solution, k):
        new_solution = solution
        for _ in range(k):
            i, j = np.random.choice(len(solution.routes), size=2, replace=False)
            new_solution = new_solution.swap(i, j)
        return new_solution

    def solve(self, max_iterations, k_max):
        current_solution = self.generate_initial_solution()
        for _ in range(max_iterations):
            k = 1
            while k <= k_max:
                candidate_solution = self.shake(current_solution, k)
                candidate_solution = self.local_search(candidate_solution)
                if candidate_solution.total_distance < current_solution.total_distance:
                    current_solution = candidate_solution
                    k = 1
                else:
                    k += 1
        return current_solution

def main():
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    demands = [0, 10, 15, 45]
    vehicle_capacity = [50, 50]

    instance = CVRPInstance(distance_matrix, demands, vehicle_capacity)
    vns = VNS(instance)
    solution = vns.solve(max_iterations=100, k_max=5)

    print("Routes:")
    for i, route in enumerate(solution.routes):
        print(f"Vehicle {i}: {route}, Distance: {solution.calculate_route_distance(route)}")
    print(f"Total distance traveled: {solution.total_distance}")

if __name__ == '__main__':
    main()
