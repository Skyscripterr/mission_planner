from typing import Optional, List

class IntervalNode:
    """A single node inside our Interval Tree."""
    def __init__(self, start: int, end: int, data_id: int):
        # The time range this node represents
        self.start = start
        self.end = end
        self.data_id = data_id # Which airspace restriction does this belong to?
        
        # What is the absolute maximum end-time in this subtree?
        # This is the MAGIC that makes the tree fast!
        self.max_end = end 
        
        # Links to children nodes
        self.left: Optional['IntervalNode'] = None
        self.right: Optional['IntervalNode'] = None

class IntervalTree:
    """
    TEACHING MOMENT: Interval Tree
    
    Imagine a calendar where you have lots of meetings (Intervals).
    If someone asks, "Is 2:00 PM to 3:00 PM free?", you could check EVERY single meeting 
    one by one. But if you have 10,000 meetings, that takes a long time (O(N)).
    
    An Interval Tree organizes meetings like a family tree (a Binary Search Tree). 
    It sorts them by their `start` time.
    
    The secret trick: Every node remembers the `max_end` time of all the meetings 
    below it. So, if we are looking for a conflict, and a branch's `max_end` is 
    BEFORE our meeting even starts, we can skip searching that entire branch! 
    This makes checking conflicts super fast (O(log N)).
    """
    
    def __init__(self):
        self.root: Optional[IntervalNode] = None

    def insert(self, start: int, end: int, data_id: int):
        """Adds a new time window to the tree."""
        if self.root is None:
            self.root = IntervalNode(start, end, data_id)
        else:
            self._insert(self.root, start, end, data_id)

    def _insert(self, node: IntervalNode, start: int, end: int, data_id: int):
        # Step 1: Standard Binary Search Tree insertion (sort by start time)
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
                
        # Step 2: The Magic Trick! Update the max_end of the current node
        if node.max_end < end:
            node.max_end = end

    def find_overlap(self, start: int, end: int) -> Optional[int]:
        """
        Checks if a given time window overlaps with anything in the tree.
        Returns the data_id of the conflicting restriction, or None if it's free!
        """
        return self._find_overlap(self.root, start, end)

    def _find_overlap(self, node: Optional[IntervalNode], start: int, end: int) -> Optional[int]:
        # If we reached an empty leaf, there is no conflict here.
        if node is None:
            return None

        # Check if the current node overlaps with our target!
        # Two intervals overlap if: Target Starts BEFORE Node Ends AND Target Ends AFTER Node Starts
        if start < node.end and end > node.start:
            return node.data_id

        # If the left child exists and its max_end is AFTER our start time,
        # it means a conflict MIGHT exist down the left branch. So we search left!
        if node.left is not None and node.left.max_end > start:
            return self._find_overlap(node.left, start, end)

        # Otherwise, the conflict (if any) MUST be down the right branch.
        return self._find_overlap(node.right, start, end)
