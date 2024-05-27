import numpy as np

def calculate_route_distance(route, distance_matrix):
    distance = 0
    for i in range(len(route) - 1):
        distance += distance_matrix[route[i]][route[i+1]]
    return distance

def nearest_neighbor(distance_matrix, capacity, demand, depot=0):
    num_customers = len(distance_matrix) - 1
    num_vehicles = len(capacity)

    routes = [[] for _ in range(num_vehicles)]
    remaining_capacity = capacity.copy()
    visited = [False] * (num_customers + 1)
    current_capacity = capacity.copy()

    current_node = depot

    while True:
        min_distance = np.inf
        nearest_customer = None
        nearest_vehicle = None

        for vehicle in range(num_vehicles):
            if current_capacity[vehicle] > 0:
                for customer in range(1, num_customers + 1):
                    if not visited[customer] and distance_matrix[current_node][customer] < min_distance and current_capacity[vehicle] >= demand[customer]:
                        min_distance = distance_matrix[current_node][customer]
                        nearest_customer = customer
                        nearest_vehicle = vehicle

        if nearest_customer is None:
            break

        if current_capacity[nearest_vehicle] >= demand[nearest_customer]:
            routes[nearest_vehicle].append(nearest_customer)
            visited[nearest_customer] = True
            current_capacity[nearest_vehicle] -= demand[nearest_customer]
            current_node = nearest_customer
        else:
            current_node = depot

    return routes, current_capacity

def main():
    distance_matrix = [
        [0, 10, 15, 20],  
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    capacity = [50, 50]  
    demand = [0, 10, 50, 40]  
    depot = 0 

    routes, remaining_capacity = nearest_neighbor(distance_matrix, capacity, demand, depot)

    total_distance = 0
    for i, route in enumerate(routes):
        route_distance = calculate_route_distance([depot] + route + [depot], distance_matrix)
        total_distance += route_distance
        print(f"Route for vehicle {i}: {route}, Distance: {route_distance}, Remaining Capacity: {remaining_capacity[i]}")

    print(f"Total distance traveled: {total_distance}")

if __name__ == '__main__':
    main()
