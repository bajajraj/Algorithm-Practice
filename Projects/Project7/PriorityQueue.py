"""
Rajaditya Shrikishan Bajaj
Project 5 - PriorityHeaps - Solution Code
CSE 331 Fall 2020
Dr. Sebnem Onsay
"""

from typing import List, Any
from PriorityNode import PriorityNode, MaxNode, MinNode


class PriorityQueue:
    """
    Implementation of a priority queue - the highest/lowest priority elements
    are at the front (root). Can act as a min or max-heap.
    """

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   DO NOT MODIFY the following attributes/functions
    #   Modify only below indicated line
    __slots__ = ["_data", "_is_min"]

    def __init__(self, is_min: bool = True):
        """
        Constructs the priority queue
        :param is_min: If the priority queue acts as a priority min or max-heap.
        """
        self._data = []
        self._is_min = is_min

    def __str__(self) -> str:
        """
        Represents the priority queue as a string
        :return: string representation of the heap
        """
        return F"PriorityQueue [{', '.join(str(item) for item in self._data)}]"

    __repr__ = __str__

    def to_tree_str(self) -> str:
        """
        Generates string representation of heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""

        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self._data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    def is_min_heap(self) -> bool:
        """
        Check if priority queue is a min or a max-heap
        :return: True if min-heap, False if max-heap
        """
        return self._is_min

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line
    def __len__(self) -> int:
        """
        Determine the amount of nodes on the heap
        :return: the amount of nodes in the priority queue.
        """
        return len(self._data)

    def empty(self) -> bool:
        """
        Checks if the heap is empty
        :returns: bool - True if Empty, else False
        """
        if len(self._data) == 0:
            return True
        return False

    def peek(self) -> PriorityNode:
        """
        Gets the root node
        :return:  None if heap is empty, else root node
        """
        if self.empty():
            return None
        return self._data[0]

    def get_left_child_index(self, index: int) -> int:
        """
        Gets the specified parent node's left child index
        :param index: index of parent node
        :return: left child's index if exist, otherwise None
        """
        position = 2 * index + 1
        if position < len(self._data):
            return position
        return None

    def get_right_child_index(self, index: int) -> int:
        """
        Gets the specified parent node's right child index
        :param index: index of parent node
        :return: right child's index if exist, otherwise None
        """
        position = 2 * index + 2
        if position < len(self._data):
            return position
        return None

    def get_parent_index(self, index: int) -> int:
        """
        Gets the specified child node's parent index
        :param index: index of the child node
        :return: parent's index is exist, otherwise none
        """
        if index == 0:
            return None
        return (index - 1) // 2

    def push(self, priority: Any, val: Any) -> None:
        """
        Inserts a node with the specified priority/value pair onto the heap
        :param priority: node's priority
        :param val: node's value
        :return: None
        """
        if self.is_min_heap():
            self._data.append(MinNode(priority, val))
        else:
            self._data.append(MaxNode(priority, val))
        self.percolate_up(len(self._data) - 1)

    def pop(self) -> PriorityNode:
        """
        Removes the top priority node from heap (min or max element)

        :return: Min or Max node, the root node of heap
        """
        if len(self._data) == 0:
            return None
        self._data[0], self._data[len(self._data) - 1] = self._data[len(self._data) - 1], self._data[0]
        item = self._data.pop()
        self.percolate_down(0)
        return item

    def get_minmax_child_index(self, index: int) -> int:
        """
        Gets the specified parent's min (min-heap) or max (max-heap) child index

        :param index: index of parent's child
        :return: Index of min child (if min-heap) or max child (if max-heap)
                 or None if invalid
        """
        if len(self._data) == 0:
            return None

        if self.get_left_child_index(index) is None and self.get_right_child_index(index) is None:
            return None

        if self.get_right_child_index(index) is None:
            return self.get_left_child_index(index)

        if self.get_left_child_index(index) is None:
            return self.get_right_child_index(index)

        right_index = self.get_right_child_index(index)
        left_index = self.get_left_child_index(index)

        if self._data[right_index] < self._data[left_index]:
            return right_index

        if self._data[left_index] < self._data[right_index]:
            return left_index

    def percolate_up(self, index: int) -> None:
        """
        Moves a node in the queue/heap up to its correct position
        (level in the tree).
        :param index: index of node to percolate up.
        :return: None
        """
        if index < len(self._data):
            parent = self.get_parent_index(index)

            if index > 0 and self._data[index] < self._data[parent]:
                self._data[index], self._data[parent] = self._data[parent], self._data[index]
                self.percolate_up(parent)

    def percolate_down(self, index: int) -> None:
        """
        Moves a node in the queue/heap down to its correct position
        (level in the tree).
        :param index: index of node to percolate down
        :return: None
        """
        if self.get_left_child_index(index) is not None:
            left = self.get_left_child_index(index)
            small_child = left
            if self.get_right_child_index(index) is not None:
                right = self.get_right_child_index(index)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[index]:
                self._data[index], self._data[small_child] = self._data[small_child], self._data[index]
                self.percolate_down(small_child)


class MaxHeap:
    """
    Implementation of a max-heap - the highest value is at the front (root).

    Initializes a PriorityQueue with is_min set to False.

    Uses the priority queue to satisfy the min heap properties by initializing
    the priority queue as a max-heap, and then using value as both the priority
    and value.
    """

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   DO NOT MODIFY the following attributes/functions
    #   Modify only below indicated line

    __slots__ = ['_pqueue']

    def __init__(self):
        """
        Constructs a priority queue as a max-heap
        """
        self._pqueue = PriorityQueue(False)

    def __str__(self) -> str:
        """
        Represents the max-heap as a string
        :return: string representation of the heap
        """
        # NOTE: This hides implementation details
        return F"MaxHeap [{', '.join(item.value for item in self._pqueue._data)}]"

    __repr__ = __str__

    def to_tree_str(self) -> str:
        """
        Generates string representation of heap in Breadth First Ordering Format
        :return: String to print
        """
        return self._pqueue.to_tree_str()

    def __len__(self) -> int:
        """
        Determine the amount of nodes on the heap
        :return: Length of the data inside the heap
        """
        return len(self._pqueue)

    def empty(self) -> bool:
        """
        Checks if the heap is empty
        :returns: True if empty, else False
        """
        return self._pqueue.empty()

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line
    def peek(self) -> Any:
        """
        function that gives the value of the top node.
        :return: root nodes value
        """
        if self._pqueue.peek() is not None:
            return self._pqueue.peek().value
        return None

    def push(self, val: Any) -> None:
        """
        Inserts a node with the specified value onto the heap

        :param val: node's value
        :return: None
        """
        self._pqueue.push(val, val)

    def pop(self) -> Any:
        """
        this function removes th root node and gives it value.
        :return: the root node value
        """
        if self._pqueue.peek() is not None:
            return self._pqueue.pop().value
        return None


class MinHeap(MaxHeap):
    """
    Implementation of a max-heap - the highest value is at the front (root).

    Initializes a PriorityQueue with is_min set to True.

    Inherits from MaxHeap because it uses the same exact functions, but instead
    has a priority queue with a min-heap.
    """

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   DO NOT MODIFY the following attributes/functions
    __slots__ = []

    def __init__(self):
        """
        Constructs a priority queue as a min-heap
        """
        super().__init__()
        self._pqueue._is_min = True


def heap_sort(array: List[Any]) -> None:
    """
    Sort array in-place using heap sort algorithm w/ max-heap
    :param array: list to be sorted
    :return: None
    """
    max_heap = MaxHeap()
    for item in array:
        max_heap.push(item)

    for i in range(len(array) - 1, -1, -1):
        array[i] = max_heap.pop()


def current_medians(array: List[int]) -> List[int]:
    """
    Function to find the median of the stream of numbers in
    the list.
    :param array: the list of which median to be found.
    :return: the list containing medians.
    """
    if not array:
        return []

    # Init min and max heaps with correct functions
    min_heap = MinHeap()
    max_heap = MaxHeap()
    median_list = []

    for i in array:
        if min_heap.empty() and max_heap.empty():
            max_heap.push(i)
        else:
            if i < median:
                max_heap.push(i)

            else:
                min_heap.push(i)

        if len(max_heap) > len(min_heap) + 1:
            root = max_heap.pop()
            min_heap.push(root)

        if len(min_heap) > len(max_heap) + 1:
            root = min_heap.pop()
            max_heap.push(root)

        if len(max_heap) == len(min_heap):
            median = (min_heap.peek() + max_heap.peek())/2
            median_list.append(median)

        elif len(max_heap) > len(min_heap):
            median = max_heap.peek()
            median_list.append(median)

        else:
            median = min_heap.peek()
            median_list.append(median)

    return median_list
