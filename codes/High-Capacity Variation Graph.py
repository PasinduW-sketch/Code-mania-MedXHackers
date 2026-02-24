import sys
from collections import deque


def maxFlow(num_nodes, edges, source, sink):
    """
    Calculate the maximum flow from source to sink using the Edmonds-Karp algorithm.
    
    Edmonds-Karp is an implementation of the Ford-Fulkerson method that uses
    Breadth-First Search (BFS) to find augmenting paths. This guarantees
    O(V * E^2) time complexity.
    
    Args:
        num_nodes: Total number of nodes in the graph (nodes are 1-indexed)
        edges: List of tuples (from_node, to_node, capacity) representing directed edges
        source: The source node where flow originates
        sink: The sink node where flow terminates
    
    Returns:
        The maximum possible flow value from source to sink.
    """
    # Initialize residual capacity matrix
    # residual[u][v] represents the remaining capacity from node u to node v
    residual = [[0] * (num_nodes + 1) for _ in range(num_nodes + 1)]
    
    # Build the residual graph from the given edges
    for from_node, to_node, capacity in edges:
        residual[from_node][to_node] += capacity
    
    total_flow = 0
    
    while True:
        # Use BFS to find an augmenting path from source to sink
        parent = [-1] * (num_nodes + 1)
        parent[source] = source
        
        queue = deque([source])
        
        # BFS to find the shortest augmenting path
        while queue and parent[sink] == -1:
            current = queue.popleft()
            
            for neighbor in range(1, num_nodes + 1):
                # Check if there's residual capacity and neighbor is not visited
                if residual[current][neighbor] > 0 and parent[neighbor] == -1:
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        # If no augmenting path found, we're done
        if parent[sink] == -1:
            break
        
        # Find the minimum residual capacity along the path (bottleneck)
        path_flow = float('inf')
        node = sink
        while node != source:
            path_flow = min(path_flow, residual[parent[node]][node])
            node = parent[node]
        
        # Update residual capacities along the augmenting path
        node = sink
        while node != source:
            previous = parent[node]
            # Decrease forward edge capacity
            residual[previous][node] -= path_flow
            # Increase backward edge capacity (allow flow cancellation)
            residual[node][previous] += path_flow
            node = previous
        
        total_flow += path_flow
    
    return total_flow


def main():
    """
    Reads input from standard input and computes maximum flow.
    
    Input Format:
        - First line: two integers n (number of nodes) and m (number of edges)
        - Next m lines: three integers u, v, c (edge from u to v with capacity c)
        - Last line: two integers s (source) and t (sink)
    """
    input_data = sys.stdin.buffer.read().split()
    index = 0
    
    num_nodes = int(input_data[index])
    index += 1
    num_edges = int(input_data[index])
    index += 1
    
    edges = []
    for _ in range(num_edges):
        from_node = int(input_data[index])
        index += 1
        to_node = int(input_data[index])
        index += 1
        capacity = int(input_data[index])
        index += 1
        edges.append((from_node, to_node, capacity))
    
    source = int(input_data[index])
    index += 1
    sink = int(input_data[index])
    index += 1
    
    result = maxFlow(num_nodes, edges, source, sink)
    print(result)


if __name__ == "__main__":
    main()
