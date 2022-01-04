"""
Lukas Richters & Sean Nguyen
Inspired by: Anna De Biasi & Andrew McDonald
CC11 - Tries - Solution Code
CSE 331 Spring 2021
Professor Sebnem Onsay
"""

from __future__ import annotations
from typing import List
from collections import defaultdict


class Node:
    """
    The node class is used to implement a trie.
    """

    __slots__ = ["children", "is_end"]

    def __init__(self) -> None:
        """
        Constructs a Node.
        """
        self.children = defaultdict(Node)
        self.is_end = False

    def __str__(self) -> str:
        """
        Returns a string representation of the node.
        """
        return "Node"

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        """
        return str(self)


class Trie:
    """
    A trie is a type of tree data structure designed to allow for similar functionality to a
    Python dictionary.
    """

    __slots__ = ["root", "out_list"]

    def __init__(self) -> None:
        """
        Initializes a root and a size.
        """
        self.root = Node()
        self.out_list = []

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        :param word: the word to insert.
        :return: None
        """

        # If no word is given, nothing to insert.
        if len(word) == 0:
            return
        # Get the root node.
        node = self.root

        # Iterate through each character in the word to set the given value.
        for char in word:
            node = node.children[char]

        # Mark the end of the word
        node.is_end = True

    def __str__(self) -> str:
        """
        Returns a string representation of the trie.
        :return: None
        """

        def pretty_print(node: Node, prefix: str, string: str) -> str:

            for child, c_node in node.children.items():
                if c_node.is_end > 0:
                    string += f"{prefix}{child}, "
                else:
                    string = pretty_print(c_node, prefix + child, string)

            return string

        return pretty_print(self.root, '', 'Trie<')[:-2] + '>'

    def __repr__(self) -> str:
        """
        Returns a string representation of the trie.
        :return: None
        """
        return str(self)

    def enemy_revealer_helper(self, root, key_list, limit_checker=0, out_str=""):
        """
        helper function for enemy_revelar
        """

        if limit_checker >= len(key_list):
            if not root.is_end:
                for c in root.children:
                    if c.isupper():
                        continue
                    else:
                        new_str = out_str + c
                        self.enemy_revealer_helper(root.children[c], key_list, limit_checker, new_str)
            else:
                self.out_list.append(out_str)

        else:
            for c in root.children:
                if c == key_list[limit_checker]:
                    new_str = out_str + c
                    new_limit = limit_checker + 1
                    self.enemy_revealer_helper(root.children[c], key_list, new_limit, new_str)

                elif c.isupper():
                    continue

                else:
                    new_str = out_str + c
                    self.enemy_revealer_helper(root.children[c], key_list, limit_checker, new_str)


def enemy_revealer(trie: Trie, key: str) -> List[str]:
    root = trie.root
    key_list = []
    for i in key:
        key_list.append(i)
    trie.enemy_revealer_helper(root, key_list)
    ret_list = trie.out_list
    # enemy_revealer_helper(trie, root, key_list, ret_list)
    return ret_list
