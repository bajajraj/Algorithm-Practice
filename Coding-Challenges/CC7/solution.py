"""
Rajaditya Shrikishan Bajaj
Coding Challenge 7
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from __future__ import annotations  # allow self-reference


class TreeNode:
    """Tree Node that contains a value as well as left and right pointers"""

    def __init__(self, value: int, left: TreeNode = None, right: TreeNode = None):
        self.value = value
        self.left = left
        self.right = right


def insert_and_ret_left_max(root, key, left_max=None):
    """
    This function inserts key in the binary search tree that we will make and will help in
    finding the maximum value on the left that is smaller than the given key.

    :root: The root we will insert in BinarySearchTree
    :key: the value we will insert.
    :left_max: the variable that will keep track of the max value
    :return: the required value
    """

    if root is None:
        return TreeNode(key), left_max
    if key < root.value:
        root.left, left_max = insert_and_ret_left_max(root.left, key, left_max)
    elif key > root.value:
        root.right, left_max = insert_and_ret_left_max(root.right, key, root.value)
    return root, left_max


def rewind_combo(points):
    """
    In this function, each element of the input list should be replaced with
    the greatest element that is smaller than the current element and is to its left.

    :param points: Python integer list of size n representing hit points
    :return: A new list with the greatest smaller predecessor for each element in the list
    """

    new_list = []
    root = None
    for num, word in enumerate(points):
        root, value = insert_and_ret_left_max(root, word)
        new_list.append(value)

    return new_list
