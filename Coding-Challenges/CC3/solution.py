"""
Rajaditya Shrikishan Bajaj
Coding Challenge 3
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import List


def finding_best_bot(bots_list: List[int]) -> int:
    """
    This function helps in finding the index of the greatest
    integer in the list with help of recursion and binary search.
    param: bots_list: List[int]: The python list of integer
           of size n.
    return: index of the greatest integer.
    Time Complexity: O(log(n))
    """

    def finding_best_bot_helper(start: int, end: int):
        """
        This is the helper recursion function for finding_best_bot
        that takes data from the bots_list
        param: start: The starting index from where we want to look in our list
               end: The ending index for our list
        return: The index of the greatest integer.
        """
        if start == end:
            return end + 1  # to see we have reached to the position where the
            # len(list) = 1. return the len(list).

        mid = (start + end) // 2  # the point where we are looking at.

        # it is the point where we have found our greatest integer. + 1 for answer
        if bots_list[mid] > bots_list[mid + 1] and bots_list[mid] > bots_list[mid - 1]:
            return mid + 1

        # if the integer is present in the right part of out mid.
        if bots_list[mid + 1] > bots_list[mid] > bots_list[mid - 1]:
            return finding_best_bot_helper(mid + 1, end)
        else: # if in left part of out list.
            return finding_best_bot_helper(start, mid - 1)

    return finding_best_bot_helper(0, len(bots_list) - 1)
