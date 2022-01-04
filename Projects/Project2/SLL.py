"""
Project 1
CSE 331 S21 (Onsay)
Rajaditya Shrikishan Bajaj
DLL.py
"""

from typing import TypeVar  # For use in type hinting
from Project2.Node import Node

# Type Declarations
T = TypeVar('T')  # generic type
SLL = TypeVar('SLL')  # forward declared


class RecursiveSinglyLinkList:
    """
    Recursive implementation of an SLL
    """

    __slots__ = ['head']

    def __init__(self) -> None:
        """
        Initializes an `SLL`
        :return: None
        """
        self.head = None

    def __repr__(self) -> str:
        """
        Represents an `SLL` as a string
        """
        return self.to_string(self.head)

    def __str__(self) -> str:
        """
        Represents an `SLL` as a string
        """
        return self.to_string(self.head)

    def __eq__(self, other: SLL) -> bool:
        """
        Overloads `==` operator to compare SLLs
        :param other: right hand operand of `==`
        :return: `True` if equal, else `False`
        """
        comp = lambda n1, n2: n1 == n2 and (comp(n1.next, n2.next) if (n1 and n2) else True)
        return comp(self.head, other.head)

    # ============ Modify below ============ #

    def to_string(self, curr: Node) -> str:
        """
        It generates and returns a string of
        list starting at curr.
        :param curr: the current node
        :return: the string
        :Time complexity: O(n^2)
        """
        # if it is not the last element
        if curr is not None and curr.next is not None:
            return str(curr.val) + " --> " + self.to_string(curr.next)
        elif curr is not None:  # last element in list
            return str(curr.val)  # str(curr.val) is to make a string
        return "None"  # if empty, return None

    def length(self, curr: Node) -> int:
        """
        It determines the number of nodes in the list
        Time complexity: O(n)
        :param curr: the current node starting from head
        :return: an integer
        """
        # counts the number of nodes
        if curr is not None:
            return 1 + self.length(curr.next)
        return 0  # if empty list, return None

    def sum_list(self, curr: Node) -> T:
        """
        It calculates the sum of the values in the node
        Time complexity: O(n)
        :param curr: the current or the head node
        :return: an integer
        """
        # sums the value in the list
        if curr is not None:
            return curr.val + self.sum_list(curr.next)
        return 0

    def push(self, value: T) -> None:
        """
        Inserts the given value at the back of the linked
        list.
        Time complexity: O(n)
        :param value: the value to be insert
        :return: None
        """
        # if the list is empty, create a new.
        if self.head is None:
            curr_node = Node(value)
            self.head = curr_node
            return

        def push_inner(curr: Node) -> Node:
            """
            This is the helper function for push. It inserts
            the given value into the linked list that has head curr
            Time complexity: O(n)
            :param curr: the head node
            :return: the end node
            """
            # if it is last node
            if curr.next is None:
                new_node = Node(value)  # create a new node
                curr.next = Node(value)  # set the next value to new node
                return new_node
            else:
                push_inner(curr.next)

        push_inner(self.head)

    def remove(self, value: T) -> None:
        """
        remove the first node in the list with the given node.
        Time complexity: O(n)
        :param value: the value of the node to be removed
        :return: None
        """
        # if empty list, return None
        if self.head is None:
            return
        # if head to be removed
        if self.head.next is None and self.head.val == value:
            self.head = self.head.next
            return

        def remove_inner(curr: Node) -> Node:
            """
            This is the helper function for remove_inner.
            It remove the first node in the list with the given node.
            Time complexity: O(n)
            :param curr: the head node
            :return: the node to be removed
            """
            # the value to be removed, it skips the list
            if curr is not None and curr.val == value:
                return curr.next
            elif curr is not None:
                curr.next = remove_inner(curr.next)
            return curr

        self.head = remove_inner(self.head)

    def remove_all(self, value: T) -> None:
        """
        It removes all the the nodes in the list with given value
        Time complexity: O(n)
        :param value: the value to be removed
        :return: None
        """

        def remove_all_inner(curr):
            """
            This is the helper function for remove_inner.
            It remove all node in the list with the given node.
            Time complexity: O(n)
            :param curr: the head node
            :return: the node to be removed
            """
            # if it is empty list
            if curr is None:
                return None
            else:
                # if curr.val to be removed
                if curr.val == value:
                    return remove_all_inner(curr.next)
                else:
                    curr.next = remove_all_inner(curr.next)
                    return curr

        self.head = remove_all_inner(self.head)

    def search(self, value: T) -> bool:
        """
        It looks for the value in the linked list
        Time complexity: O(n)
        :param value: the value to be searched
        :return: true if the value is found, else false
        """

        def search_inner(curr):
            """
            This is the helper function for search.
            It looks for the value in the linked list
            Time complexity: O(n)
            :param curr: the head node
            :return: true if the value is found, else found
            """
            # if the list is empty.
            if curr is None:
                return False
            elif curr.val == value:
                return True
            else:
                return search_inner(curr.next)

        return search_inner(self.head)

    def count(self, value: T) -> int:
        """
        It counts and returns the number of times a given value
        occurred in the linked list.
        Time complexity: O(n)
        :param value: value to be searched
        :return: the number of time value is there (int)
        """

        def count_inner(curr):
            """
            It is the inner function counts and returns the
            number of times a given value occurred in the linked list.
            Time complexity: O(n)
            :param curr: the head node
            :return: the number of time value is there (int)
            """
            # counts the number of nodes
            if curr is None:  # if empty list or at none node
                return 0
            elif curr.val == value:
                return 1 + count_inner(curr.next)
            else:
                return 0 + count_inner(curr.next)

        return count_inner(self.head)

    def reverse(self, curr: Node) -> Node:
        """
        This function reveres the list.
        Time complexity: O(n)
        :param curr: the head node of the list
        :return: the node in the reverse order.
        """
        # if we are at the last element.
        if curr is None or curr.next is None:
            self.head = curr  # make it to head
            return curr
        temp = self.reverse(curr.next)
        curr.next.next = curr
        curr.next = None
        return temp  # changes the head and last node


def crafting():
    """
    Given two linked lists, recipe and pockets, determine if
    the values in the recipe list are contained in the pockets list.
    If all the values in recipe are present in pockets, they will
    be consumed, and therefore must be removed from pockets. Return
    True if the pockets contain enough ingredients to complete the
    recipe, False otherwise.
    Time complexity: O(rp)
    return: true or false
    """

    pass
