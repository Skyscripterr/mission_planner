from typing import Optional, List

class IntervalNode:
    def __init__(self, start: int, end: int, data_id: int):
        self.start = start
        self.end = end
        self.data_id = data_id
        
    
        self.max_end = end 
        
        self.left: Optional['IntervalNode'] = None
        self.right: Optional['IntervalNode'] = None

class IntervalTree:
    def __init__(self):
        self.root: Optional[IntervalNode] = None

    def insert(self, start: int, end: int, data_id: int):

        if self.root is None:
            self.root = IntervalNode(start, end, data_id)
        else:
            self._insert(self.root, start, end, data_id)

    def _insert(self, node: IntervalNode, start: int, end: int, data_id: int):
       
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
      
        if node.max_end < end:
            node.max_end = end

    def find_overlap(self, start: int, end: int) -> Optional[int]:
     
        return self._find_overlap(self.root, start, end)

    def _find_overlap(self, node: Optional[IntervalNode], start: int, end: int) -> Optional[int]:
        if node is None:
            return None

        if start < node.end and end > node.start:
            return node.data_id

     
        if node.left is not None and node.left.max_end > start:
            return self._find_overlap(node.left, start, end)

        return self._find_overlap(node.right, start, end)
