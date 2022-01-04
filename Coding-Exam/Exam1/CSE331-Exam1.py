from typing import TypeVar, List, Tuple

T = TypeVar("T")            # represents generic type
Node = TypeVar("Node")      # represents a Node object (forward-declare to use in Node __init__)

class Node:
    """
    Implementation of a doubly linked list node.
    Do not modify.
    """
    __slots__ = ["value", "next", "prev"]

    def __init__(self, value: T, next: Node = None, prev: Node = None) -> None:
        """
        Construct a doubly linked list node.
        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        """
        self.next = next
        self.prev = prev
        self.value = value

    def __repr__(self) -> str:
        """
        Represents the Node as a string.
        :return: string representation of the Node.
        """
        return str(self.value)

    def __str__(self) -> str:
        """
        Represents the Node as a string.
        :return: string representation of the Node.
        """
        return str(self.value)


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.
        :return: None.
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.
        :return: string representation of the DLL.
        """
        result = ""
        node = self.head
        while node is not None:
            result += str(node)
            if node.next is not None:
                result += " <-> "
            node = node.next
        return result

    def __str__(self) -> str:
        """
        Represent the DLL as a string.
        :return: string representation of the DLL.
        """
        return repr(self)

    def count_nodes(self):
        current_node = self.head
        while current_node:
            self.size += 1
            current_node.next
        return self.size
    
def remove_middle(data: DLL) -> DLL:
    """
    Removes the middle node(s) from a doubly linked list
    :param data: a DLL
    :return: the modified DLL
    """
    if data.head is None:
        return data
    else:
        count = data.size

        if count % 2 != 0:
            mid = (count + 1) // 2
            # Iterate through list till current points to mid position
            current_odd = data.head
            for i in range(1, mid):
                current_odd = current_odd.next

            # If middle node is head of the list
            if current_odd == data.head:
                if data.size == 1:
                    data.head = None
                    data.tail = None
                    data.size -= 1
                    return data
                data.head = current_odd.next
            # If middle node is tail of the list
            elif current_odd == data.tail:
                data.tail = data.tail.previous
            else:
                current_odd.prev.next = current_odd.next
                current_odd.next.prev = current_odd.prev
            current_odd = None
            data.size -= 1
            return data

        else:
            mid_one = count // 2
            # Iterate through list till current points to mid position
            current_one = data.head
            for i in range(1, mid_one):
                current_one = current_one.next

            # If middle node is head of the list
            if current_one == data.head:
                data.head = current_one.next
            # If middle node is tail of the list
            elif current_one == data.tail:
                data.tail = data.tail.previous
            else:
                current_one.prev.next = current_one.next
                current_one.next.prev = current_one.prev
            current_one = None
            data.size -= 1

            mid_two = (data.size + 2) // 2

            current_two = data.head

            for i in range(1, mid_two):
                current_two = current_two.next

            # If middle node is head of the list
            if current_two == data.head:
                if data.size == 1:
                    data.head = None
                    data.tail = None
                    data.size -= 1
                    return data
                data.head = current_two.next
            # If middle node is tail of the list
            elif current_two == data.tail:
                data.tail.prev.next = None
                data.tail = data.tail.prev
            else:
                current_two.prev.next = current_two.next
                current_two.next.prev = current_two.prev

            data.size -= 1
            current_two = None

            return data
