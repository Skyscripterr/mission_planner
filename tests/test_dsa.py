import pytest
from app.algorithms.topological_sort import topological_sort, CircularDependencyError
from app.algorithms.interval_tree import IntervalTree

def test_topological_sort_simple():
    # A -> B -> C
    vertices = [1, 2, 3]
    edges = [(1, 2), (2, 3)]
    result = topological_sort(vertices, edges)
    assert result == [1, 2, 3]

def test_topological_sort_complex():
    # 1 -> 2, 1 -> 3, 2 -> 4, 3 -> 4
    vertices = [1, 2, 3, 4]
    edges = [(1, 2), (1, 3), (2, 4), (3, 4)]
    result = topological_sort(vertices, edges)
    # Both [1, 2, 3, 4] and [1, 3, 2, 4] are valid
    assert result[0] == 1
    assert result[3] == 4
    assert set(result[1:3]) == {2, 3}

def test_topological_sort_cycle():
    # A -> B -> A
    vertices = [1, 2]
    edges = [(1, 2), (2, 1)]
    with pytest.raises(CircularDependencyError):
        topological_sort(vertices, edges)

def test_interval_tree_simple():
    tree = IntervalTree()
    tree.insert(10, 20, 1) # restriction 1: 10 to 20
    tree.insert(30, 40, 2) # restriction 2: 30 to 40
    
    # Free window
    assert tree.find_overlap(21, 29) is None
    
    # Overlap with restriction 1
    assert tree.find_overlap(15, 25) == 1
    
    # Overlap with restriction 2
    assert tree.find_overlap(35, 36) == 2
    
    # Window covers multiple
    assert tree.find_overlap(5, 50) is not None

def test_interval_tree_edge_cases():
    tree = IntervalTree()
    tree.insert(10, 20, 1)
    
    # Exact start/end match (non-overlapping by convention in some systems, 
    # but here we check start < node.end and end > node.start)
    # [10, 20] and [20, 30] -> 20 < 20 is False. No overlap.
    assert tree.find_overlap(20, 30) is None
    assert tree.find_overlap(5, 10) is None
    
    # But [19, 21] should overlap
    assert tree.find_overlap(19, 21) == 1
