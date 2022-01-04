"""
Name:
Project 3 - Hybrid Sorting
Developed by Sean Nguyen and Andrew Haas
Based on work by Zosha Korzecke and Olivia Mikola
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
import math
from typing import TypeVar, List, Callable

T = TypeVar("T")  # represents generic type


def merge(data_one, data_two, data, threshold,
          comparator: Callable[[T, T], bool] = lambda x, y: x <= y):
    """
    It is function that helps merge_sort to merge the divided smaller
    arrays and also to sort them.

    :param data_one: the left side of the list.
    :param data_two: the right side of the list.
    :param data: the combined list.
    :param threshold: an integer whether to count inversion.
    :param comparator: a lambda argument for comparing data.
    :return: None, else an int giving the number of inversions if threshold == 0.
    """
    inversion = 0
    i = j = 0
    while i + j < len(data):
        if j == len(data_two) or (i < len(data_one) and comparator(data_one[i], data_two[j])):
            data[i + j] = data_one[i]
            i = i + 1
        else:
            data[i + j] = data_two[j]
            if threshold == 0:     # to count the number of inversions.
                inversion += (len(data_one) - i)
            j = j + 1

    return inversion


def merge_sort(data: List[T], threshold: int = 0,
               comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> int:
    """
    This function sorts a given list in ascending or descending order taking help
    of merge function. It also returns the number of inversion_count if the threshold
    given for the function is greater than zero.

    :param data: the given input list to be sorted.
    :param threshold: an int which tells when to use insertion_sort and it also gives
                      information about the initialising inversion_count if threshold == 0.
    :param comparator: a lambda argument for comparing data.
    :return: None if threshold != 0 else returns the inversion count.
    :Time Complexity: O(nlog(n)).
    """
    count_one = count_two = count_three = 0
    n = len(data)
    if n < 2:
        return 0  # we are returning 0 because threshold will be 0.
    if len(data) <= threshold != 0:
        insertion_sort(data)
    else:
        mid = n // 2
        data_one = data[0:mid]
        data_two = data[mid:n]
        count_one = merge_sort(data_one, count_three, comparator)
        count_two = merge_sort(data_two, count_three, comparator)

        count_three = merge(data_one, data_two, data, threshold, comparator)

        if threshold == 0:
            return count_one + count_two + count_three
    return 0


def insertion_sort(data: List[T], comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> None:
    """
    This is a sorting function which uses insertion sort algorithm. It returns a sorted list.

    :param data: the given input list to be sorted.
    :param comparator: a lambda argument for comparing data.
    :return: None (a sorted list).
    :Time complexity: O(n^2).
    """
    for i in range(1, len(data)):
        j = i  # 0 <= j
        while j > 0 and comparator(data[j], data[j - 1]):
            temp = data[j]
            data[j] = data[j - 1]
            data[j - 1] = temp
            j = j - 1


def hybrid_sort(data: List[T], threshold: int,
                comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> None:
    """
    It is a wrapper function to call merge_sort() as a Hybrid Sorting Algorithm. It
    returns a list in sorted order.

    :param data: the given input list to be sorted.
    :param threshold: the value for switching between insertion_sort() and merge_sort().
    :param comparator: a lambda function which compares data.
    :return: None (a the given input list into a sorted list).
    :Time complexity: O(nlog(n)).
    """
    merge_sort(data, threshold, comparator)


def inversions_count(data: List[T]) -> int:
    """
    It is wrapper function to call merge_sort() on a copy of data to retrieve
     the inversion count.

     :param data: the given input list.
     :return: an int giving the number of inversion count.
     :Time complexity: O(nlog(n)).
    """
    new_list = []
    for ls in range(0, len(data)):
        new_list.append(data[ls])
    return merge_sort(new_list, 0)


def reverse_sort(data: List[T], threshold: int) -> None:
    """
    It is a wrapper function to use merge_sort() to sort the data in reverse.

    :param data: the given input list to be reverse sorted.
    :param threshold: the value to switch between insertion_sort() and merge_sort().
    :return: None (the reverse sorted list).
    :Time complexity: O(nlog(n)).
    """
    comparator: Callable[[T, T], bool] = lambda x, y: x >= y
    merge_sort(data, threshold, comparator)


def password_rate(password: str) -> float:
    """
    Rate a given password via the equation given in the problem statement. The
    is (sqrt(length of string) * sqrt(number of unique characters) + number
    of inversion_count()).

    :param password: the string to be rated.
    :return: the floated point rating of the string.
    :Time complexity: O(p*log(p)) - where p is the password length.
    """
    password_set = set(password)
    password_list = []

    for i in range(0, len(password)):
        password_list.append(password[i])

    inversion = inversions_count(password_list)
    password_length = len(password)
    rate = float(((password_length ** 0.5) * (len(password_set) ** 0.5)) + inversion)

    return rate


def password_sort(data: List[str]) -> None:
    """
    This function sorts a list of passwords by their ratings
    (the results from password_rate()).

    :param data: the list of password to be sorted.
    :return: None (the sorted password list based on password_rate()).
    :Time complexity: O(n*p*log(p) + n*log(n)), where n is the number of passwords
                      in the list and p is the average password length.
    """
    tuple_list = []

    for ls in range(0, len(data)):
        password = data[ls]
        rate = password_rate(password)
        tuple_list.append((rate, password))

    merge_sort(tuple_list, 0, lambda x, y: x[0] >= y[0])

    for lv in range(0, len(tuple_list)):
        data[lv] = tuple_list[lv][1]