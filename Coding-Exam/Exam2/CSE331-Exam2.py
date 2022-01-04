from typing import List, Generator, TypeVar
from copy import deepcopy

BSTNode = TypeVar('BSTNode') # BST Node Type
BST = TypeVar('BST')         # BST Type
T = TypeVar('T')             # Generic Type

class BSTNode:
    """
    BST Node Class:

    Attributes:
        val  : int
        left : BSTNode
        right: BSTNode
    """

    __slots__ = ['val', 'left', 'right']

    def __init__(self, val: int) -> None:
        """ Initialize BST Node """
        self.val = val
        self.left = self.right = None

    def __str__(self):
        return str(self.val)

    __repr__ = __str__

    def __eq__(self, other: BSTNode):
        return self.val == other.val

class BST:
    """
    BST Class: Contains only unique nodes

    Attributes:
        root: BSTNode
        size: int
    """

    __slots__ = ['root', 'size']

    def __init__(self, vals: List[int] = []) -> None:
        """ Initialize BST """
        self.root = None
        self.size = 0
        for val in vals:
            self.insert(self.root, val)

    def __eq__(self, other: BST) -> bool:
        """ Equality Comparator for BSTs """
        comp = lambda n1, n2: n1==n2 and ((comp(n1.left, n2.left) and comp(n1.right, n2.right)) if (n1 and n2) else True)
        return self.size == other.size and comp(self.root, other.root)

    def insert(self, root: BSTNode, val: int) -> None:
        """ Insert Node in BST """
        if root is None:
            self.root = BSTNode(val)
        elif val < root.val:
            if root.left is None:
                root.left = BSTNode(val)
            else:
                return self.insert(root.left, val)
        elif val > root.val:
            if root.right is None:
                root.right = BSTNode(val)
            else:
                return self.insert(root.right, val)
        self.size += 1

    def break_tree(self, val1: int, val2: int) -> BST:
        """ Creates copy of tree with two specified nodes swapped """

        copy = BST()
        copy.size = self.size
        copy.root = deepcopy(self.root)

        def find(root, val):
            if val < root.val:
                return find(root.left, val)
            elif val > root.val:
                return find(root.right, val)
            return root

        node1 = find(copy.root, val1)
        node2 = find(copy.root, val2)

        node1.val, node2.val = node2.val, node1.val

        return copy

#=== complete the following function ===#

def repair_tree(tree: BST) -> None:
    root = tree.root
    prev = [None, None, None]

    def repair_tree_helper(root):
        if root is None:
            return
        else:
            repair_tree_helper(root.left)
            if prev[0] is None:
                prev[0] = root
            else:
                if root.val <= prev[0].val:
                    if prev[1] is None:
                        prev[1] = prev[0]
                    prev[2] = root
                prev[0] = root
            repair_tree_helper(root.right)

    repair_tree_helper(root)
    prev[1].val, prev[2].val = prev[2].val, prev[1].val