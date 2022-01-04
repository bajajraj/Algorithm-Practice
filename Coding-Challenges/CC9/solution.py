"""
Name:
Coding Challenge 9
CSE 331 Spring 2021
Professor Sebnem Onsay
"""

from typing import List, Tuple
import queue


class Dungeon:
    """
    Represents a dungeon made of rooms connected by hallways
    Implemented as an adjacency matrix
    """

    __slots__ = ['adjacency_matrix']

    def __init__(self, rooms: List[int], hallways: List[Tuple[int, int]]) -> None:
        self.adjacency_matrix = [[0] * len(rooms) for _ in range(len(rooms))]
        for hall in hallways:
            self._add_connecting_hallway(*hall)

    def _add_connecting_hallway(self, start_room: int, end_room: int) -> None:
        """
        Adds a hallway to the dungeon
        :param start_room: start room
        :param end_room: end room
        :return: None
        """
        self.adjacency_matrix[start_room][end_room] = self.adjacency_matrix[end_room][start_room] = 1

    def get_connecting_rooms(self, current_room: int) -> List[int]:
        """
        Gets a list of rooms connected to the current room
        :param current_room: current room represented by an index in the matrix
        :return: List of connected, adjacent rooms
        """
        connecting_rooms = []
        for connected_room, required_stamina in enumerate(self.adjacency_matrix[current_room]):
            if required_stamina > 0:
                connecting_rooms.append(connected_room)
        return connecting_rooms

    def get_required_stamina(self, start_room: int, end_room: int) -> int:
        """
        Gets the required stamina between two edges
        :param start_room: First room at the end of a hallway
        :param end_room: Second room at the other end of a hallway
        :return: Stamina of hallway as an int
            will be 1 if the rooms are connected by a single hallway,
            0 if the rooms are not connected by a single hallway
        """
        return self.adjacency_matrix[start_room][end_room]


def dungeon_path_finder(dungeon: Dungeon, start: int, end: int) -> List[int]:
    """
    helper function that keeps the track of the path taken by the
    nodes to reach the destination from the starting point.

    :param dungeon: the class dungeon
    :param start: the starting room
    :param end: the final room
    :return: the list containing the rooms.
    """
    node_queue = queue.SimpleQueue() # it will help in rooms adjacent to given node.
    node_queue.put(start)
    path_queue = queue.SimpleQueue()
    path_queue.put((str(start)))
    visited = {}  # it is dictionary which will will keep track of room visited.
    while not node_queue.empty():
        vertex = node_queue.get()
        path = path_queue.get()
        if vertex not in visited:
            if vertex == end:
                return path  # we have reached our ending point
            visited[vertex] = "visited"
            for neighbor in dungeon.get_connecting_rooms(vertex):
                node_queue.put(neighbor)
                new_value = path + ' ' + str(neighbor)
                path_queue.put((new_value))


def convert_str_to_int(path: List[str]) -> List[int]:
    """
    Helper function which helps in converting a list of strings
    into a list of ints.
    :param path: the list of strings
    :return: the list of ints
    """
    path = path.split()
    new_list = []
    for i in path:
        new_list.append(int(i))
    return new_list


def calculate_stamina(dungeon: Dungeon, path_taken: List[int]) -> int:
    """
    It is a helper function which helps in calculating stamina
    of the person who has taken the given path.

    :param dungeon: the Dungeon class given to us.
    :param path_taken: the list containing our path.
    :return: the stamina used by us.
    """
    stamina = 0
    i = 1
    while i < len(path_taken):
        stamina += dungeon.get_required_stamina(path_taken[i - 1], path_taken[i])
        i += 1
    return stamina


def dungeon_escape(dungeon: Dungeon, start_room: int, end_room: int,
                   stamina_limit: int) -> Tuple[List[int], int]:
    """
    It is the function that finds a path from a start room to an end room
    while also calculating the stamina used.

    :param dungeon: the Dungeon class given to us.
    :param start_room: the starting room
    :param end_room: the end room
    :param stamina_limit: the max stamina we can use.
    :return: the tuple containing the list of path taken, empty if no path
             exits, and the zero stamina if no path exists or the max stamina
             is less than the required stamina.
    """
    path = dungeon_path_finder(dungeon, start_room, end_room)
    if path is None:
        return [], 0

    path = convert_str_to_int(path)
    stamina = calculate_stamina(dungeon, path)
    if stamina_limit < stamina:
        return [], 0
    else:
        return path, stamina
