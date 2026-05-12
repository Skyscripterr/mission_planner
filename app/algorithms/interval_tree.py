from typing import Optional, List

class IntervalNode:
    """Internal node representing a closed interval in the Interval Tree."""
    def __init__(self, start: int, end: int, data_id: int):
        self.start = start
        self.end = end
        self.data_id = data_id
        
        # Max end-time in the subtree rooted at this node for efficient pruning.
        self.max_end = end 
        
        self.left: Optional['IntervalNode'] = None
        self.right: Optional['IntervalNode'] = None

class IntervalTree:
    """
    An Interval Tree for efficient O(log N) overlap queries.
    
    This implementation follows the augmented Binary Search Tree pattern,
    sorting nodes by their start time and maintaining a `max_end` metadata
    field for subtree pruning during search operations.
    """
    
    def __init__(self):
        self.root: Optional[IntervalNode] = None

    def insert(self, start: int, end: int, data_id: int):
        """Inserts an interval [start, end] into the tree."""
        if self.root is None:
            self.root = IntervalNode(start, end, data_id)
        else:
            self._insert(self.root, start, end, data_id)

    def _insert(self, node: IntervalNode, start: int, end: int, data_id: int):
        # Standard BST insertion based on interval start time
        if start < node.start:
            if node.left is None:
                node.left = IntervalNode(start, end, data_id)
            else:
                self._insert(node.left, start, end, data_id)
        else:
            if node.right is None:
                node.right = IntervalNode(start, end, data_id)
            else:
                self._insert(node.right, start, end, data_id)
                
        # Maintain max_end invariant
        if node.max_end < end:
            node.max_end = end

    def find_overlap(self, start: int, end: int) -> Optional[int]:
        """
        Queries the tree for any interval overlapping with [start, end].
        Returns the data_id of the first overlap found, or None.
        """
        return self._find_overlap(self.root, start, end)

    def _find_overlap(self, node: Optional[IntervalNode], start: int, end: int) -> Optional[int]:
        if node is None:
            return None

        # Overlap check for closed intervals
        if start < node.end and end > node.start:
            return node.data_id

        # Search left subtree if its max_end could potentially contain an overlap
        if node.left is not None and node.left.max_end > start:
            return self._find_overlap(node.left, start, end)

        # Fallback to right subtree
        return self._find_overlap(node.right, start, end)
