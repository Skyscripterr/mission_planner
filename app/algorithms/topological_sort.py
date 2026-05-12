from typing import List, Dict, Set

class CircularDependencyError(Exception):
    """Exception raised when a cycle is detected in the dependency graph."""
    pass

def topological_sort(vertices: List[int], edges: List[tuple[int, int]]) -> List[int]:
    """
    Performs a Topological Sort using Kahn's Algorithm.
    
    Time Complexity: O(V + E)
    Space Complexity: O(V + E)
    
    :param vertices: List of unique vertex identifiers.
    :param edges: List of directed edges (u, v) where u is a prerequisite of v.
    :return: A linearly ordered list of vertices satisfying all dependencies.
    :raises CircularDependencyError: If the graph contains at least one cycle.
    """
    
    # Initialize in-degree counts and adjacency list for graph representation
    in_degree: Dict[int, int] = {v: 0 for v in vertices}
    adjacency_list: Dict[int, List[int]] = {v: [] for v in vertices}
    
    for src, dst in edges:
        if src in adjacency_list and dst in in_degree:
            adjacency_list[src].append(dst)
            in_degree[dst] += 1
            
    # Identify sources (vertices with no incoming edges)
    queue: List[int] = [v for v in vertices if in_degree[v] == 0]
    sorted_order: List[int] = []
    
    while queue:
        u = queue.pop(0) 
        sorted_order.append(u)
        
        for v in adjacency_list[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # Validate result: If sorted_order contains fewer vertices than original set, a cycle exists.
    if len(sorted_order) != len(vertices):
        raise CircularDependencyError(
            "Graph validation failed: Cycle detected in dependencies."
        )
        
    return sorted_order
