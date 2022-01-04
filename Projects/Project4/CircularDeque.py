"""
Project 4
CSE 331 S21 (Onsay)
Name
CircularDeque.py
"""

from __future__ import annotations
from typing import TypeVar, List
import re

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
CircularDeque = TypeVar("CircularDeque")  # represents a CircularDeque object


class CircularDeque:
    """
    Class representation of a Circular Deque
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = [], capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param capacity: amount of space in the deque
        """
        self.capacity: int = capacity
        self.size: int = len(data)

        self.queue: list[T] = [None] * capacity
        self.front: int = None
        self.back: int = None

        for index, value in enumerate(data):
            self.queue[index] = value
            self.front = 0
            self.back = index

    def __str__(self) -> str:
        """
        Provides a string represenation of a CircularDeque
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        string = f"CircularDeque <{self.queue[self.front]}"
        current_index = self.front + 1 % self.capacity
        while current_index <= self.back:
            string += f", {self.queue[current_index]}"
            current_index = (current_index + 1) % self.capacity
        return string + ">"

    def __repr__(self) -> str:
        """
        Provides a string represenation of a CircularDeque
        :return: the instance as a string
        """
        return str(self)

    # ============ Modify below ============ #

    def __len__(self) -> int:
        """
        Returns the length/size of the circular deque.
        :param: self - a CircularDeque
        :return: int
        :Time Complexity: O(1)
        :Space Complexity: O(1)
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the circular deque is empty
        :param: self - a CircularDeque
        :return: True if empty, otherwise false
        :Time complexity: O(1)
        :Space complexity: O(1)
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        Returns the first element in the circular deque
        :param: self - a CircularDeque
        :return: the front element
        :Time complexity: O(1)
        :Space Complexity: O(1)
        """
        if self.size == 0:
            return

        return self.queue[self.front]

    def back_element(self) -> T:
        """
        Returns the last element in the circular deque.
        :param: self - a CircularDeque
        :return: the last element
        :Time complexity: O(1)
        :Space complexity: O(1)
        """
        if self.size == 0:
            return

        return self.queue[self.back]

    def front_enqueue(self, value: T) -> None:
        """.
        Adds value to the front of the circular deque
        :param value: T: value to add into the circular deque
        :Returns: None
        :Time complexity: O(1)*
        :Space complexity: O(1)*
        """
        if self.size == 0:
            self.front = self.back = 0
        else:
            self.front = (self.front - 1) % len(self.queue)

        self.queue[self.front] = value
        self.size += 1

        # check weather to grow
        if self.size == self.capacity:
            self.grow()

    def back_enqueue(self, value: T) -> None:
        """
        Adds value to the end of the circular deque
        param value: T: value to add into the circular deque
        Returns: None
        Time complexity: O(1)*
        Space complexity: O(1)*
        """
        if self.size == 0:  # if size == 0, we would need to reinstate NoneType
            self.back = self.front = 0
        else:
            self.back = (self.back + 1) % self.capacity

        # check weather to shrink
        self.queue[self.back] = value
        self.size += 1

        if self.size == self.capacity:
            self.grow()

    def front_dequeue(self) -> T:
        """
        Removes the item at the front of the circular deque
        :Returns: item at the front of the circular deque, None if empty
        :Time complexity: O(1)*
        :Space complexity: O(1)*
        """
        if self.size == 0:
            return

        # get popped item and adjust object attributes
        answer = self.queue[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1

        # check weather to shrink
        if 0 < self.size <= self.capacity // 4 and self.capacity // 2 >= 4:
            self.shrink()

        return answer

    def back_dequeue(self) -> T:
        """
        Removes the item at the end of the circular deque
        Time complexity: O(1)*
        Space complexity: O(1)*
        Returns: item at the end of the circular deque, None if empty
        """
        if self.size == 0:
            return

        # get popped item and adjust object attributes
        data = self.queue[self.back]
        self.back = (self.back - 1) % self.capacity
        self.size -= 1

        # check weather to shrink
        if 0 < self.size <= self.capacity // 4 and self.capacity // 2 >= 4:
            self.shrink()

        return data

    def grow(self) -> None:
        """
        If the current size is equal to the current capacity,
        double the capacity of the circular deque
        Time complexity: O(n)
        Space complexity: O(n)
        Returns: None
        """
        old_queue = self.queue
        self.queue = [None] * (self.capacity * 2)
        self_head = self.front

        for k in range(self.size):
            self.queue[k] = old_queue[self_head]
            self_head = (1 + self_head) % self.capacity

        self.front = 0
        self.back = self.size - 1
        self.capacity = self.capacity * 2

    def shrink(self) -> None:
        """
        If the current size is less than or equal to one fourth the current
        capacity, and 1/2 the current capacity is greater than or equal to 4,
        halves the capacity.
        Time complexity: O(n)
        Space complexity: O(n)
        Returns: None
        """
        old_queue = self.queue
        self.queue = [None] * (self.capacity // 2)
        self_head = self.front

        for k in range(self.size):
            self.queue[k] = old_queue[self_head]
            self_head = (1 + self_head) % self.capacity

        self.front = 0
        self.back = self.size - 1
        self.capacity //= 2


def LetsPassTrains102(infix: str) -> (float, str):
    """
    It converts a mathematical expression from in-fix notation to
    post-fix notation by using
    shunting yard algorithm.
    :Time complexity: O(n)
    :Space complexity: O(n)
    :Inputs: string - a valid mathematical expression in infix notation.
    :return: a tuple containing the calculation and the postfix string
    """
    if not infix:  # if the string is empty
        return 0, ""

    is_operator = {'+', '-', '*', '/', '(', ')', '^'}  # set of operators
    priority_dict = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # dictionary having priorities

    cd_deque = CircularDeque()  # initially stack empty

    # through regex we are parsing the string
    regex = r"\-*\d+\.\d+|\-\d+|[\(\)\-\^\*\+\/]|(?<!-)\d+|\w"

    regex_list = re.findall(regex, infix)

    output = []  # initially output empty

    for num, word in enumerate(regex_list):

        if word not in is_operator:  # if an operand then
            # put it directly in postfix expression
            output.append(word)

        elif word == '(':  # else operators should be put in stack
            cd_deque.back_enqueue('(')

        elif word == ')':
            while cd_deque.is_empty() is False and cd_deque.back_element() != '(':
                output.append(cd_deque.back_dequeue())
            cd_deque.back_dequeue()

        else:
            # lesser priority can't be on top on higher or
            # equal priority so pop and put in output
            while cd_deque.is_empty() is False and cd_deque.back_element() != '(' \
                    and priority_dict[word] <= \
                    priority_dict[cd_deque.back_element()]:
                output.append(cd_deque.back_dequeue())
            cd_deque.back_enqueue(word)

    while not cd_deque.is_empty():
        output.append(cd_deque.back_dequeue())

    postfix = ''
    # it will convert our list into a string format
    for num, out_str in enumerate(output):
        if num != len(output) - 1:
            postfix += out_str
            postfix += ' '
        else:
            postfix += out_str

    stack = CircularDeque()

    for i, sign in enumerate(output):

        if sign == "+":
            first_element = stack.back_dequeue()
            second_element = stack.back_dequeue()
            if second_element is None:
                stack.back_enqueue(0 + float(first_element))
            else:
                stack.back_enqueue(float(second_element) + float(first_element))

        elif sign == "*":
            first_element = stack.back_dequeue()
            second_element = stack.back_dequeue()
            stack.back_enqueue(float(second_element) * float(first_element))

        elif sign == "/":
            first_element = stack.back_dequeue()
            second_element = stack.back_dequeue()
            stack.back_enqueue(float(second_element) / float(first_element))

        elif sign == "-":
            first_element = stack.back_dequeue()
            second_element = stack.back_dequeue()
            if second_element is None:
                stack.back_enqueue(0 - float(first_element))
            else:
                stack.back_enqueue(float(second_element) - float(first_element))

        elif sign == "^":
            first_element = stack.back_dequeue()
            second_element = stack.back_dequeue()

            stack.back_enqueue(float(second_element) ** float(first_element))

        else:
            stack.back_enqueue(float(sign))

    return stack.back_dequeue(), postfix
