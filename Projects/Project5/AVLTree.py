"""
Project 5
CSE 331 S21 (Onsay)
Your Name
AVLTree.py
"""

import queue
from typing import TypeVar, Generator, List, Tuple

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
Node = TypeVar("Node")  # represents a Node object (forward-declare to use in Node __init__)
AVLWrappedDictionary = TypeVar("AVLWrappedDictionary")  # represents a custom type used in application


####################################################################################################


class Node:
    """
    Implementation of an AVL tree node.
    Do not modify.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["value", "parent", "left", "right", "height"]

    def __init__(self, value: T, parent: Node = None,
                 left: Node = None, right: Node = None) -> None:
        """
        Construct an AVL tree node.

        :param value: value held by the node object
        :param parent: ref to parent node of which this node is a child
        :param left: ref to left child node of this node
        :param right: ref to right child node of this node
        """
        self.value = value
        self.parent, self.left, self.right = parent, left, right
        self.height = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"

    def __str__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"


####################################################################################################


class AVLTree:
    """
    Implementation of an AVL tree.
    Modify only below indicated line.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty AVL tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree as a string. Inspired by Anna De Biasi (Fall'20 Lead TA).

        :return: string representation of the AVL tree
        """
        if self.origin is None:
            return "Empty AVL Tree"

        # initialize helpers for tree traversal
        root = self.origin
        result = ""
        q = queue.SimpleQueue()
        levels = {}
        q.put((root, 0, root.parent))
        for i in range(self.origin.height + 1):
            levels[i] = []

        # traverse tree to get node representations
        while not q.empty():
            node, level, parent = q.get()
            if level > self.origin.height:
                break
            levels[level].append((node, level, parent))

            if node is None:
                q.put((None, level + 1, None))
                q.put((None, level + 1, None))
                continue

            if node.left:
                q.put((node.left, level + 1, node))
            else:
                q.put((None, level + 1, None))

            if node.right:
                q.put((node.right, level + 1, node))
            else:
                q.put((None, level + 1, None))

        # construct tree using traversal
        spaces = pow(2, self.origin.height) * 12
        result += "\n"
        result += f"AVL Tree: size = {self.size}, height = {self.origin.height}".center(spaces)
        result += "\n\n"
        for i in range(self.origin.height + 1):
            result += f"Level {i}: "
            for node, level, parent in levels[i]:
                level = pow(2, i)
                space = int(round(spaces / level))
                if node is None:
                    result += " " * space
                    continue
                if not isinstance(self.origin.value, AVLWrappedDictionary):
                    result += f"{node} ({parent} {node.height})".center(space, " ")
                else:
                    result += f"{node}".center(space, " ")
            result += "\n"
        return result

    def __str__(self) -> str:
        """
        Represent the AVL tree as a string. Inspired by Anna De Biasi (Fall'20 Lead TA).

        :return: string representation of the AVL tree
        """
        return repr(self)

    def height(self, root: Node) -> int:
        """
        Return height of a subtree in the AVL tree, properly handling the case of root = None.
        Recall that the height of an empty subtree is -1.

        :param root: root node of subtree to be measured
        :return: height of subtree rooted at `root` parameter
        """
        return root.height if root is not None else -1

    def left_rotate(self, root: Node) -> Node:
        """
        Perform a left rotation on the subtree rooted at `root`. Return new subtree root.

        :param root: root node of unbalanced subtree to be rotated.
        :return: new root node of subtree following rotation.
        """
        if root is None:
            return None

        # pull right child up and shift right-left child across tree, update parent
        new_root, rl_child = root.right, root.right.left
        root.right = rl_child
        if rl_child is not None:
            rl_child.parent = root

        # right child has been pulled up to new root -> push old root down left, update parent
        new_root.left = root
        new_root.parent = root.parent
        if root.parent is not None:
            if root is root.parent.left:
                root.parent.left = new_root
            else:
                root.parent.right = new_root
        root.parent = new_root

        # handle tree origin case
        if root is self.origin:
            self.origin = new_root

        # update heights and return new root of subtree
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))
        return new_root

    ########################################
    # Implement functions below this line. #
    ########################################

    def right_rotate(self, root: Node) -> Node:
        """
        Perform a right rotation on the subtree rooted at `root`. Return new subtree root.

        :param root: root node of unbalanced subtree to be rotated.
        :return: new root node of subtree following rotation.
        """
        if root is None:
            return None

        # pull left child up and shift left-right child across tree, update parent
        new_root, lr_child = root.left, root.left.right
        root.left = lr_child
        if lr_child is not None:
            lr_child.parent = root
        # left child has been pulled up to the new root -> push old root down right, update parent
        new_root.right = root
        new_root.parent = root.parent
        if root.parent is not None:
            if root is root.parent.left:
                root.parent.left = new_root
            else:
                root.parent.right = new_root
        root.parent = new_root

        # handle tree origin case
        if root is self.origin:
            self.origin = new_root

        # update heights and return new root of the subtree
        root.height = 1 + max(self.height(root.right), self.height(root.left))
        new_root.height = 1 + max(self.height(new_root.right), self.height(new_root.left))
        return new_root

    def balance_factor(self, root: Node) -> int:
        """
        Compute the balance factor of the subtree rooted at root.

        :param root: root node of subtree on which to compute the balance factor
        :return: int representing the balance factor of root.
        """
        if not root:
            return 0

        left_height = -1
        if root.left is not None:
            left_height = root.left.height
        right_height = -1
        if root.right is not None:
            right_height = root.right.height
        return left_height - right_height

    def rebalance(self, root: Node) -> Node:
        """
        Rebalance the subtree rooted at root (if necessary) and return the new
        root of the resulting subtree.

        :param root: root node of subtree to be rebalanced
        :return: root of the new tree after rebalancing
        """
        self.height(root)
        balance = self.balance_factor(root)
        if balance == -2:
            if self.balance_factor(root.right) == 1:
                # Double rotation case
                self.right_rotate(root.right)
            return self.left_rotate(root)
        if balance == 2:
            if self.balance_factor(root.left) == -1:
                # Double rotation case
                self.left_rotate(root.left)
            return self.right_rotate(root)
        return root

    def insert(self, root: Node, val: T) -> Node:
        """
        Insert a node with val into the subtree rooted at root,
        returning the root node of the balanced subtree after insertion.

        :param root: Node: The root Node of the subtree in which to insert val.
        :param val: T: The value to be inserted in the subtree rooted at root.
        :return: Root of new subtree after insertion and rebalancing (could be the original root).
        """
        if self.origin is None:
            self.origin = Node(val)
            self.size += 1
            return self.origin

        if root.value == val:
            return self.rebalance(root)
        if val < root.value and root.left is not None:
            self.insert(root.left, val)
        elif val > root.value and root.right is not None:
            self.insert(root.right, val)
        elif val < root.value and root.left is None:
            root.left = Node(val, parent=root)
            self.size += 1
        elif val > root.value and root.right is None:
            root.right = Node(val, parent=root)
            self.size += 1

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        # root_node = self.rebalance(root)
        return self.rebalance(root)

    def min(self, root: Node) -> Node:
        """
        Find and return the Node with the smallest value in the subtree rooted at root.

        :param root: Node: The root Node of the subtree in which to search for a minimum.
        :returns: Node object containing the smallest value in the subtree rooted at root.
        """
        if root is None:
            return None
        if root.left is None:
            return root
        return self.min(root.left)

    def max(self, root: Node) -> Node:
        """
        Find and return the Node with the largest value in the subtree rooted at root.

        :param root: Node: The root Node of the subtree in which to search for a maximum.
        :returns: Node object containing the largest value in the subtree rooted at root.
        """
        if root is None:
            return None
        if root.right is None:
            return root
        return self.max(root.right)

    def search(self, root: Node, val: T) -> Node:
        """
        Find and return the Node with the value val in the subtree rooted at root.

        :param root: The root Node of the subtree in which to search for val.
        :param val: The value being searched in the subtree rooted at root.
        :returns: Node object containing val if it exists, else the Node
                object below which val would be inserted as a child.
        """
        if self.origin is None:
            return None

        if root.value == val:
            return root

        if val < root.value:
            if root.left is None:
                return root
            return self.search(root.left, val)

        if val > root.value:
            if root.right is None:
                return root
            return self.search(root.right, val)

    def inorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform an inorder (left, current, right) traversal of the subtree
        rooted at root using a Python generator.

        :param root: The root Node of the subtree currently being traversed.
        :returns: Generator object which yields Node objects only
        """
        if root is None:
            return None
            # return if the tree is empty

        yield from self.inorder(root.left)
        yield root
        yield from self.inorder(root.right)

    def preorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a preorder (current, left, right) traversal of the subtree
        rooted at root using a Python generator.

        :param root: The root Node of the subtree currently being traversed.
        :returns: Generator object which yields Node objects only
        """
        if root is None:
            return None
            # return if empty tree

        yield root
        yield from self.preorder(root.left)
        yield from self.preorder(root.right)

    def postorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a postorder (left, right, current) traversal of the subtree
        rooted at root using a Python generator.

        :param root: The root Node of the subtree currently being traversed.
        :returns: Generator object which yields Node objects only
        """
        if root is None:
            return None
            # return if tree is empty

        yield from self.postorder(root.left)
        yield from self.postorder(root.right)
        yield root
        # yields left subtrees, right subtrees, then root

    def levelorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a levelorder (breadth-first) traversal of the subtree
        rooted at root using a Python generator.

        :param root: The root Node of the subtree currently being traversed.
        :returns: Generator object which yields Node objects only
        """
        if root is None:
            return None
        output = queue.SimpleQueue()
        output.put(root)

        while output.empty() is False:
            root1 = output.get()
            yield root1

            if root1.left:
                output.put(root1.left)
            if root1.right:
                output.put(root1.right)

    def remove(self, root: Node, val: T) -> Node:
        """
        Remove the node with value val from the subtree rooted at root, and
        return the root of the balanced subtree following removal.

        :param root: The root Node of the subtree from which to delete val.
        :param val: The value to be deleted from the subtree rooted at root.
        :returns: Root of new subtree after removal and rebalancing (could be the original root).
        """
        if self.origin is None:
            return None

        if root is None:
            return self.rebalance(root)

        if root.value < val:
            root.right = self.remove(root.right, val)

        elif root.value > val:
            root.left = self.remove(root.left, val)

        elif root.value == val:
            if root.right is None and root.left is None:
                parent_node = root.parent
                if parent_node is None:
                    self.origin = None
                elif parent_node.right is not None and parent_node.right.value == val:
                    parent_node.right = None
                else:
                    parent_node.left = None
                self.size -= 1
                root.height = 1 + max(self.height(root.left), self.height(root.right))
                return self.rebalance(root)

            if root.right is None or root.left is None:
                parent_node = root.parent
                if root.right is not None:
                    child_node = root.right
                else:
                    child_node = root.left
                if parent_node is None:
                    self.origin = child_node
                elif parent_node.right is not None and parent_node.right.value == val:
                    parent_node.right = child_node
                else:
                    parent_node.left = child_node
                child_node.parent = parent_node
                self.size -= 1
                root.height = 1 + max(self.height(root.left), self.height(root.right))
                return self.rebalance(root)

            max_left = self.max(root.left)
            root.left = self.remove(root.left, max_left.value)
            root.value = max_left.value

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return self.rebalance(root)


####################################################################################################


class AVLWrappedDictionary:
    """
    Implementation of a helper class which will be used as tree node values in the
    NearestNeighborClassifier implementation.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["key", "dictionary"]

    def __init__(self, key: float) -> None:
        """
        Construct a AVLWrappedDictionary with a key to search/sort on and a dictionary to hold data.

        :param key: floating point key to be looked up by.
        """
        self.key = key
        self.dictionary = {}

    def __repr__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        return f"key: {self.key}, dict: {self.dictionary}"

    def __str__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        return f"key: {self.key}, dict: {self.dictionary}"

    def __eq__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement == operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating whether keys of AVLWrappedDictionaries are equal
        """
        return self.key == other.key

    def __lt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement < operator to compare 2 AVLWrappedDictionarys by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key < other.key

    def __gt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement > operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key > other.key


class NearestNeighborClassifier:
    """
    Implementation of a one-dimensional nearest-neighbor classifier with AVL tree lookups.
    Modify only below indicated line.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["resolution", "tree"]

    def __init__(self, resolution: int) -> None:
        """
        Construct a one-dimensional nearest neighbor classifier with AVL tree lookups.
        Data are assumed to be floating point values in the closed interval [0, 1].

        :param resolution: number of decimal places the data will be rounded to, effectively
                           governing the capacity of the model - for example, with a resolution of
                           1, the classifier could maintain up to 11 nodes, spaced 0.1 apart - with
                           a resolution of 2, the classifier could maintain 101 nodes, spaced 0.01
                           apart, and so on - the maximum number of nodes is bounded by
                           10^(resolution) + 1.
        """
        self.tree = AVLTree()
        self.resolution = resolution

        # pre-construct lookup tree with AVLWrappedDictionary objects storing (key, dictionary)
        # pairs, but which compare with <, >, == on key only
        for i in range(10 ** resolution + 1):
            w_dict = AVLWrappedDictionary(key=(i / 10 ** resolution))
            self.tree.insert(self.tree.origin, w_dict)

    def __repr__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return f"NNC(resolution={self.resolution}):\n{self.tree}"

    def __str__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return f"NNC(resolution={self.resolution}):\n{self.tree}"

    def fit(self, data: List[Tuple[float, str]]) -> None:
        """
        REPLACE
        """
        new_list = []
        for i in range(len(data)):
            value = data[i][0]
            string = data[i][1]
            new_list.append((round(value, 1), string))

    def predict(self, x: float, delta: float) -> str:
        """
        REPLACE
        """
        pass
