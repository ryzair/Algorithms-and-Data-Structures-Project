import heapq

class Graph:
    def __init__(self):
        self.adj_list = {}  # Dictionary to store adjacency list as a dictionary of dictionaries
        self.charging_stations = {'H', 'K', 'Q', 'T'} # Set of charging stations

    def add_edge(self, u, v, weight):
        if u not in self.adj_list:
            self.adj_list[u] = {}
        if v not in self.adj_list:
            self.adj_list[v] = {}
        
        self.adj_list[u][v] = weight
        self.adj_list[v][u] = weight  # Assuming an undirected graph

    def print_graph(self):
        for node, neighbors in self.adj_list.items():
            connections = ", ".join([f"{neighbor}: {weight}" for neighbor, weight in neighbors.items()])
            print(f"{node} : {{{connections}}}")

    def dijkstra(self, start):
        pq = [(0, start)]  # (distance, node)
        distances = {node: float('inf') for node in self.adj_list}
        distances[start] = 0
        shortest_paths = {node: [] for node in self.adj_list}
        shortest_paths[start] = [start]

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in self.adj_list[current_node].items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
                    shortest_paths[neighbor] = shortest_paths[current_node] + [neighbor]
        
        return distances, shortest_paths
    
    def shortest_path_to_ev_stations(self, start):
        distances, shortest_paths = self.dijkstra(start)
        charging_station_paths = {station: shortest_paths[station] for station in self.charging_stations}
        charging_station_distances = {station: distances[station] for station in self.charging_stations}

        most_efficient_station = min(charging_station_distances, key=charging_station_distances.get)
        most_efficient_distance = charging_station_distances[most_efficient_station]
        most_efficient_path = charging_station_paths[most_efficient_station]

        # Print all paths
        for station in self.charging_stations:
            print(f"Shortest path from {start} to {station}: {charging_station_paths[station]}, Distance: {distances[station]}")

        # Print the most efficient route
        print(f"\nMost efficient route to a charging station is to {most_efficient_station}: {most_efficient_path}, Distance: {most_efficient_distance}")

# Example usage
def main():
    graph = Graph()

    # Load data from CSV file
    csv_file_path = 'C:/Users/paula/Desktop/SUMMER 24 COURSES/Algorithims and Data Structure/Assignment 3/nodes_network.csv'

    with open(csv_file_path, 'r') as file:
        lines = file.readlines()

    header = lines[0]
    data_lines = lines[1:]

    # Add edges to the graph
    for line in data_lines:
        node1, node2, distance, charging_station = line.strip().split(',')
        distance = int(distance)
        graph.add_edge(node1, node2, distance)

    # Print the adjacency list representation of the graph
    graph.print_graph()

    # Prompt the user for the starting node
    start_node = input("Enter the starting node in Capital Letters: ")

    if start_node in graph.adj_list:
        # Find and print the shortest paths to each charging station from the starting node
        graph.shortest_path_to_ev_stations(start_node)
    else:
        print("Invalid starting node. Please enter a node that exists in the graph.")

if __name__ == "__main__":
    main()
