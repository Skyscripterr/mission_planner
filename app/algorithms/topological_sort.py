from typing import List, Dict, Set

class CircularDependencyError(Exception):
    """An error raised when mission steps depend on each other in a loop!"""
    pass

def topological_sort(vertices: List[int], edges: List[tuple[int, int]]) -> List[int]:
    """
    TEACHING MOMENT: Topological Sort (Kahn's Algorithm)
    
    Imagine you are getting dressed. You must put on your socks BEFORE your shoes. 
    You must put on your underwear BEFORE your pants.
    
    Topological Sort is an algorithm that takes a list of tasks (vertices) and a list 
    of rules like "A must happen before B" (edges), and figures out the correct order 
    to do all the tasks!
    
    If it's impossible (e.g., "Socks before Shoes" AND "Shoes before Socks"), that's 
    called a 'Cycle', and the algorithm will catch it!

    :param vertices: A list of step IDs. Example: [1, 2, 3, 4]
    :param edges: A list of pairs where (A, B) means "A must finish before B starts".
    :return: A list of step IDs in the correct order to be executed.
    """
    
    # 1. Setup the Graph! 
    # We need to know two things for every task (vertex):
    # - in_degree: How many tasks MUST happen before this task? (How many arrows point TO it?)
    # - adjacency_list: Once this task is done, what tasks does it unlock? (Arrows pointing AWAY from it)
    
    in_degree: Dict[int, int] = {v: 0 for v in vertices}
    adjacency_list: Dict[int, List[int]] = {v: [] for v in vertices}
    
    # Let's fill out our graph based on the rules (edges) provided.
    for before_step, after_step in edges:
        # Ignore edges that refer to non-existent vertices just in case
        if before_step in adjacency_list and after_step in in_degree:
            adjacency_list[before_step].append(after_step) # "before" unlocks "after"
            in_degree[after_step] += 1                     # "after" has one more requirement
            
    # 2. Find the Starting Points!
    # A task with an in_degree of 0 has NO prerequisites. We can do it right now!
    # We put all these starting tasks into a 'queue' (a waiting line).
    queue: List[int] = [v for v in vertices if in_degree[v] == 0]
    
    # 3. Process the tasks!
    sorted_order: List[int] = []
    
    while queue:
        # Take the next available task from the front of the line
        current_task = queue.pop(0) 
        
        # Add it to our final finished list!
        sorted_order.append(current_task)
        
        # Now that 'current_task' is done, look at all the tasks it unlocks
        for next_task in adjacency_list[current_task]:
            # Cross off 'current_task' as a requirement for 'next_task'
            in_degree[next_task] -= 1
            
            # If 'next_task' now has NO MORE requirements (in_degree is 0),
            # it is ready to be done! Add it to the waiting line!
            if in_degree[next_task] == 0:
                queue.append(next_task)
                
    # 4. Check for Cycles (Infinite Loops)!
    # If we finished processing but our final list doesn't contain ALL the tasks,
    # it means some tasks were stuck waiting for each other forever!
    if len(sorted_order) != len(vertices):
        raise CircularDependencyError(
            "Cycle detected! Your mission steps depend on each other in an infinite loop."
        )
        
    return sorted_order
