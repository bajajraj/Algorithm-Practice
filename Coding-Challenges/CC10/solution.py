"""
Rajaditya Shrikishan Bajaj
Coding Challenge 10
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from CC10.game import Room, Game
import queue


def count_good_dungeons(game: Game) -> int:
    """
     This function will return an integer that is equal
     to the count of how many of its subgraphs (dungeons)
     contain paths that loop back on themselves.
    :param: A graph that stores the subgraphs (dungeons)
          to check.
    :returns: An integer that represents the count of how
            many good dungeons were found
    """

    visited = {}  # there may be sub-graphs.
    good_dungeons = 0
    rooms_list = []
    for rooms in game.rooms:
        rooms_list.append(rooms)

    for rooms in rooms_list:
        if rooms.room_id in visited:
            continue
        visited[rooms.room_id] = "Visited"
        is_cyclic = False
        node_queue = queue.SimpleQueue()
        node_queue.put((rooms, Room(None)))
        while not node_queue.empty():
            vertex, last = node_queue.get()
            for rm in vertex.adjacent_rooms:
                if rm.room_id not in visited:
                    visited[rm.room_id] = "Visited"
                    node_queue.put((rm, vertex))
                elif rm.room_id != last.room_id:
                    is_cyclic = True
        if is_cyclic:
            good_dungeons += 1

    return good_dungeons
