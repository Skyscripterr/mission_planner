from typing import List, Dict, Set

class CircularDependencyError(Exception):
    pass

def topological_sort(vertices: List[int], edges: List[tuple[int, int]]) -> List[int]:
 
    
    in_degree: Dict[int, int] = {v: 0 for v in vertices}
    adjacency_list: Dict[int, List[int]] = {v: [] for v in vertices}
    
    for src, dst in edges:
        if src in adjacency_list and dst in in_degree:
            adjacency_list[src].append(dst)
            in_degree[dst] += 1
          
    queue: List[int] = [v for v in vertices if in_degree[v] == 0]
    sorted_order: List[int] = []
    
    while queue:
        u = queue.pop(0) 
        sorted_order.append(u)
        
        for v in adjacency_list[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
  
    if len(sorted_order) != len(vertices):
        raise CircularDependencyError(
            "Graph validation failed: Cycle detected in dependencies."
        )
        
    return sorted_order
