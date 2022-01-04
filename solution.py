"""
Rajaditya Shrikishan Bajaj
Coding Challenge 4
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import List


def challenger_finder(stocks_list: List[int], k: int) -> List[int]:
    """
    This function helps in finding the number of integers that are in
    k range of a given integer in list.
    param: stocks_list: List[int]: A Python list of length n, containing integers
           k: int: Integer indicating the range
    return: A Python list of length n, containing integers
    Time Complexity: O(nlog(n)) where n is the number of players
    """
    check_list = []  # creating a new list for return.

    for i in enumerate(stocks_list):
        value = stocks_list[i]
        max_val = value + k  # maximum_value of our range.
        min_val = value - k  # minimum_value of our range.
        i = 0

        for v in enumerate(stocks_list):
            if (stocks_list[v] >= min_val) and (stocks_list[v] <= max_val):
                i += 1
            else:
                continue
        check_list.append(i - 1)    # we subtract i - 1 because i contains the number itself.

    return check_list
