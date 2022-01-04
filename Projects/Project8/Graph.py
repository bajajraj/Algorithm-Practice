"""
Name:
CSE 331 FS20 (Onsay)
"""

import heapq
import itertools
import math
import queue
import random
import time
import csv
from typing import TypeVar, Callable, Tuple, List, Set

import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

T = TypeVar('T')
Matrix = TypeVar('Matrix')  # Adjacency Matrix
Vertex = TypeVar('Vertex')  # Vertex Class Instance
Graph = TypeVar('Graph')  # Graph Class Instance


class Vertex:
    """ Class representing a Vertex object within a Graph """

    __slots__ = ['id', 'adj', 'visited', 'x', 'y']

    def __init__(self, idx: str, x: float = 0, y: float = 0) -> None:
        """
        DO NOT MODIFY
        Initializes a Vertex
        :param idx: A unique string identifier used for hashing the vertex
        :param x: The x coordinate of this vertex (used in a_star)
        :param y: The y coordinate of this vertex (used in a_star)
        """
        self.id = idx
        self.adj = {}  # dictionary {id : weight} of outgoing edges
        self.visited = False  # boolean flag used in search algorithms
        self.x, self.y = x, y  # coordinates for use in metric computations

    def __eq__(self, other: Vertex) -> bool:
        """
        DO NOT MODIFY
        Equality operator for Graph Vertex class
        :param other: vertex to compare
        """
        if self.id != other.id:
            return False
        elif self.visited != other.visited:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex visited flags not equal: self.visited={self.visited},"
                  f" other.visited={other.visited}")
            return False
        elif self.x != other.x:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex x coords not equal: self.x={self.x}, other.x={other.x}")
            return False
        elif self.y != other.y:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex y coords not equal: self.y={self.y}, other.y={other.y}")
            return False
        elif set(self.adj.items()) != set(other.adj.items()):
            diff = set(self.adj.items()).symmetric_difference(set(other.adj.items()))
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex adj dictionaries not equal:"
                  f" symmetric diff of adjacency (k,v) pairs = {str(diff)}")
            return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        :return: string representing Vertex object
        """
        lst = [f"<id: '{k}', weight: {v}>" for k, v in self.adj.items()]

        return f"<id: '{self.id}'" + ", Adjacencies: " + "".join(lst) + ">"

    def __str__(self) -> str:
        """
        DO NOT MODIFY
        :return: string representing Vertex object
        """
        return repr(self)

    def __hash__(self) -> int:
        """
        DO NOT MODIFY
        Hashes Vertex into a set; used in unit tests
        :return: hash value of Vertex
        """
        return hash(self.id)

    # ============== Modify Vertex Methods Below ==============#

    def degree(self) -> int:
        """
        Returns the number of outgoing edges from this vertex
        :return: the number of edges
        """
        return len(self.adj)

    def get_edges(self) -> Set[Tuple[str, float]]:
        """
        Returns a set of tuples representing outgoing
        edges from this vertex
        :return: tuple containing edge and their weights
        """
        get_edge_set = set()
        if self.degree() == 0:
            return get_edge_set
        for key in self.adj:
            get_edge_tuple = (key, self.adj[key])
            get_edge_set.add(get_edge_tuple)
        return get_edge_set

    def euclidean_distance(self, other: Vertex) -> float:
        """
        returns the euclidean distance between self and other
        :param other: the other vertex
        :return: the euclidean distance
        """
        x_difference = (self.x - other.x) ** 2
        y_difference = (self.y - other.y) ** 2
        euclidean = (x_difference + y_difference) ** 0.5
        return euclidean

    def taxicab_distance(self, other: Vertex) -> float:
        """
        returns the taxicab distance between self and other
        :param other: the other vertex
        :return: the taxicab distance
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


class Graph:
    """ Class implementing the Graph ADT using an Adjacency Map structure """

    __slots__ = ['size', 'vertices', 'plot_show', 'plot_delay']

    def __init__(self, plt_show: bool = False, matrix: Matrix = None, csv: str = "") -> None:
        """
        DO NOT MODIFY
        Instantiates a Graph class instance
        :param: plt_show : if true, render plot when plot() is called; else, ignore calls to plot()
        :param: matrix : optional matrix parameter used for fast construction
        :param: csv : optional filepath to a csv containing a matrix
        """
        matrix = matrix if matrix else np.loadtxt(csv, delimiter=',', dtype=str).tolist() if csv else None
        self.size = 0
        self.vertices = {}

        self.plot_show = plt_show
        self.plot_delay = 0.2

        if matrix is not None:
            for i in range(1, len(matrix)):
                for j in range(1, len(matrix)):
                    if matrix[i][j] == "None" or matrix[i][j] == "":
                        matrix[i][j] = None
                    else:
                        matrix[i][j] = float(matrix[i][j])
            self.matrix2graph(matrix)

    def __eq__(self, other: Graph) -> bool:
        """
        DO NOT MODIFY
        Overloads equality operator for Graph class
        :param other: graph to compare
        """
        if self.size != other.size or len(self.vertices) != len(other.vertices):
            print(f"Graph size not equal: self.size={self.size}, other.size={other.size}")
            return False
        else:
            for vertex_id, vertex in self.vertices.items():
                other_vertex = other.get_vertex(vertex_id)
                if other_vertex is None:
                    print(f"Vertices not equal: '{vertex_id}' not in other graph")
                    return False

                adj_set = set(vertex.adj.items())
                other_adj_set = set(other_vertex.adj.items())

                if not adj_set == other_adj_set:
                    print(f"Vertices not equal: adjacencies of '{vertex_id}' not equal")
                    print(f"Adjacency symmetric difference = "
                          f"{str(adj_set.symmetric_difference(other_adj_set))}")
                    return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        :return: String representation of graph for debugging
        """
        return "Size: " + str(self.size) + ", Vertices: " + str(list(self.vertices.items()))

    def __str__(self) -> str:
        """
        DO NOT MODFIY
        :return: String representation of graph for debugging
        """
        return repr(self)

    def plot(self) -> None:
        """
        DO NOT MODIFY
        Creates a plot a visual representation of the graph using matplotlib
        """
        if self.plot_show:

            # if no x, y coords are specified, place vertices on the unit circle
            for i, vertex in enumerate(self.get_vertices()):
                if vertex.x == 0 and vertex.y == 0:
                    vertex.x = math.cos(i * 2 * math.pi / self.size)
                    vertex.y = math.sin(i * 2 * math.pi / self.size)

            # show edges
            num_edges = len(self.get_edges())
            max_weight = max([edge[2] for edge in self.get_edges()]) if num_edges > 0 else 0
            colormap = cm.get_cmap('cool')
            for i, edge in enumerate(self.get_edges()):
                origin = self.get_vertex(edge[0])
                destination = self.get_vertex(edge[1])
                weight = edge[2]

                # plot edge
                arrow = patches.FancyArrowPatch((origin.x, origin.y),
                                                (destination.x, destination.y),
                                                connectionstyle="arc3,rad=.2",
                                                color=colormap(weight / max_weight),
                                                zorder=0,
                                                **dict(arrowstyle="Simple,tail_width=0.5,"
                                                                  "head_width=8,head_length=8"))
                plt.gca().add_patch(arrow)

                # label edge
                plt.text(x=(origin.x + destination.x) / 2 - (origin.x - destination.x) / 10,
                         y=(origin.y + destination.y) / 2 - (origin.y - destination.y) / 10,
                         s=weight, color=colormap(weight / max_weight))

            # show vertices
            x = np.array([vertex.x for vertex in self.get_vertices()])
            y = np.array([vertex.y for vertex in self.get_vertices()])
            labels = np.array([vertex.id for vertex in self.get_vertices()])
            colors = np.array(
                ['yellow' if vertex.visited else 'black' for vertex in self.get_vertices()])
            plt.scatter(x, y, s=40, c=colors, zorder=1)

            # plot labels
            for j, _ in enumerate(x):
                plt.text(x[j] - 0.03 * max(x), y[j] - 0.03 * max(y), labels[j])

            # show plot
            plt.show()
            # delay execution to enable animation
            time.sleep(self.plot_delay)

    def add_to_graph(self, start_id: str, dest_id: str = None, weight: float = 0) -> None:
        """
        Adds to graph: creates start vertex if necessary,
        an edge if specified,
        and a destination vertex if necessary to create said edge
        If edge already exists, update the weight.
        :param start_id: unique string id of starting vertex
        :param dest_id: unique string id of ending vertex
        :param weight: weight associated with edge from start -> dest
        :return: None
        """
        if self.vertices.get(start_id) is None:
            self.vertices[start_id] = Vertex(start_id)
            self.size += 1
        if dest_id is not None:
            if self.vertices.get(dest_id) is None:
                self.vertices[dest_id] = Vertex(dest_id)
                self.size += 1
            self.vertices.get(start_id).adj[dest_id] = weight

    def matrix2graph(self, matrix: Matrix) -> None:
        """
        Given an adjacency matrix, construct a graph
        matrix[i][j] will be the weight of an edge between the vertex_ids
        stored at matrix[i][0] and matrix[0][j]
        Add all vertices referenced in the adjacency matrix, but only add an
        edge if matrix[i][j] is not None
        Guaranteed that matrix will be square
        If matrix is nonempty, matrix[0][0] will be None
        :param matrix: an n x n square matrix (list of lists) representing Graph as adjacency map
        :return: None
        """
        for i in range(1, len(matrix)):  # add all vertices to begin with
            self.add_to_graph(matrix[i][0])
        for i in range(1, len(matrix)):  # go back through and add all edges
            for j in range(1, len(matrix)):
                if matrix[i][j] is not None:
                    self.add_to_graph(matrix[i][0], matrix[j][0], matrix[i][j])

    def graph2matrix(self) -> Matrix:
        """
        given a graph, creates an adjacency matrix of the type described in "construct_from_matrix"
        :return: Matrix
        """
        matrix = [[None] + [v_id for v_id in self.vertices]]
        for v_id, outgoing in self.vertices.items():
            matrix.append([v_id] + [outgoing.adj.get(v) for v in self.vertices])
        return matrix if self.size else None

    def graph2csv(self, filepath: str) -> None:
        """
        given a (non-empty) graph, creates a csv file containing data necessary to reconstruct that graph
        :param filepath: location to save CSV
        :return: None
        """
        if self.size == 0:
            return

        with open(filepath, 'w+') as graph_csv:
            csv.writer(graph_csv, delimiter=',').writerows(self.graph2matrix())

    # ============== Modify Graph Methods Below ==============#

    def reset_vertices(self) -> None:
        """
        Resets visited flags of all vertices within the graph
        """
        for key in self.vertices:
            self.vertices[key].visited = False

    def get_vertex(self, vertex_id: str) -> Vertex:
        """
        Returns the Vertex object with id vertex_id
        if it exists in the graph
        :param vertex_id: the vertex to get
        :return: Returns None if no vertex with
                unique id vertex_id exists
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        return None

    def get_vertices(self) -> Set[Vertex]:
        """
        Returns a set of all Vertex objects held in the graph
        :return: Returns an empty set if no vertices are held
                in the graph
        """
        get_vertices_set = set()
        if len(self.vertices) == 0:
            return get_vertices_set
        for key in self.vertices:
            get_vertices_set.add(self.vertices[key])
        return get_vertices_set

    def get_edge(self, start_id: str, dest_id: str) -> Tuple[str, str, float]:
        """
        Returns the edge connecting the vertex with id start_id to the vertex
        with id dest_id
        :param start_id: the starting edge
        :param dest_id: the ending edge
        :return: start_id, dest_id, edge
        """
        if start_id not in self.vertices:
            return None
        if dest_id not in self.vertices:
            return None
        if dest_id in self.vertices[start_id].adj:
            return start_id, dest_id, float(self.vertices[start_id].adj[dest_id])
        return None

    def get_edges(self) -> Set[Tuple[str, str, float]]:
        """
        Returns a set of tuples representing all edges within the graph
        :return: the set containing the edges
        """
        get_edges_set = set()
        for key in self.vertices:
            for adj in self.vertices[key].adj:
                get_edges_set.add(self.get_edge(key, adj))
        return get_edges_set

    def bfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        Perform a breadth-first search beginning at vertex with id start_id
        and terminating at vertex with id end_id
        :param start_id: the starting edge
        :param target_id: the ending edge
        :return: the path traversed and the sum of weights of the path
        """
        path_taken = []
        path_dict = {}

        if start_id not in self.vertices:
            return [], 0
        if target_id not in self.vertices:
            return [], 0

        distance = {self.vertices[start_id]: 0}
        node_queue = queue.SimpleQueue()
        vertex = self.get_vertex(start_id)
        node_queue.put(vertex)
        vertex.visited = True

        while not node_queue.empty():
            vertex = node_queue.get()
            for ver in vertex.adj:
                if self.vertices[ver].visited:
                    continue
                self.vertices[ver].visited = True
                node_queue.put(self.get_vertex(ver))
                path_dict[self.vertices[ver]] = vertex
                distance[self.vertices[ver]] = vertex.adj[ver] + distance[vertex]

        if not path_dict:
            return [], 0
        if self.vertices[target_id] not in path_dict:
            return [], 0
        path_taken.append(target_id)
        vertex = self.vertices[target_id]
        start_vertex = self.vertices[start_id]
        while vertex != start_vertex:
            vertex = path_dict[vertex]
            path_taken.append(vertex.id)
        path_taken.reverse()

        distance_taken = distance[self.vertices[target_id]]
        return path_taken, distance_taken

    def dfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        Perform a depth-first search beginning at vertex with id start_id
        and terminating at vertex with id end_id
        :param start_id: the starting edge
        :param target_id: the ending edge
        :return: the path traversed and the sum of weights of the path
        """

        def dfs_inner(current_id: str, target_id: str, path: List[str] = []) \
                -> Tuple[List[str], float]:
            """
            recursive helper function for DFS.
            :param current_id: the starting edge
            :param current_id: the target edge
            :param path: the list of the path to be taken
            :return: path, distance
            """
            path.append(current_id)
            self.vertices[current_id].visited = True
            if target_id in self.vertices[current_id].adj:
                path.append(target_id)
                return path, float(self.vertices[current_id].adj[target_id])

            for i in self.vertices[current_id].adj:
                if not self.vertices[i].visited:
                    path, distance = dfs_inner(i, target_id, path)
                    distance += float(self.vertices[current_id].adj[i])
                    return path, distance
            return [], 0

        if start_id not in self.vertices:
            return [], 0
        if target_id not in self.vertices:
            return [], 0
        path, distance = dfs_inner(start_id, target_id)
        if len(path) == 1 or len(path) == 0:
            return [], 0
        return path, distance

    def detect_cycle(self) -> bool:
        """
        This function detects the cycle in the graph.
        :return: True if cycle is present, else false
        """

        def detect_cycle_inner(current_node, visited_dict, is_cyclic):
            """
            This is a helper function for detect_cycle().
            :param current_node: the present node
            :param visited_dict: the dictionary tracking the dictionary
            :param is_cyclic: list containing True or False
            """
            if is_cyclic[0]:
                return
            visited_dict[current_node] = "Visited"
            for vert_id in self.vertices[current_node].adj:
                if visited_dict[vert_id] == "Visited":
                    is_cyclic[0] = True
                    return
                if visited_dict[vert_id] == "Not Visited":
                    detect_cycle_inner(vert_id, visited_dict, is_cyclic)
                if not is_cyclic[0]:
                    continue
            visited_dict[current_node] = "Visiting"

        visited_dict = {v: "Not Visited" for v in self.vertices}
        is_cyclic = [False]

        for v in self.vertices:
            if visited_dict[v] == "Not Visited":
                detect_cycle_inner(v, visited_dict, is_cyclic)
            if is_cyclic[0]:
                return True
        return False

    def a_star(self, start_id: str, target_id: str,
               metric: Callable[[Vertex, Vertex], float]) -> Tuple[List[str], float]:
        """
        This function performs a A* search beginning at vertex with id start_id and
        terminating at vertex with id end_id.
        :param start_id: start vertex id
        :param target_id: target vertex id
        :param metric: heuristic function
        :return: the shortest distance and the path taken.
        """

        d = {}  # d[v] is upper bound from s to v
        cloud = {}  # map reachable v to its d[v] value
        pq = AStarPriorityQueue()  # vertex v will have key d[v]
        path = {}  # map from vertex to its pq locator

        # for each vertex v of the graph, add an entry to the priority queue, with
        # the source having distance 0 and all others having infinite distance
        for v in self.vertices:
            if v == start_id:
                d[self.vertices[v]] = 0
                self.vertices[v].visited = True
            else:
                d[self.vertices[v]] = float('inf')  # syntax for positive infinity
            pq.push(d[self.vertices[v]], self.vertices[v])

        while not pq.empty():
            key, u = pq.pop()
            cloud[u] = key  # its correct d[u]
            for e in u.adj:  # outgoing edges (u,v)
                v = self.vertices[e]
                if v not in cloud:
                    # perform relaxation step on edge (u,v)
                    wgt = float(self.vertices[u.id].adj[v.id])
                    if d[u] + wgt < d[v]:  # better path to v?
                        d[v] = d[u] + wgt
                        pq.update(d[v] + metric(self.vertices[target_id], v), v)
                        path[self.vertices[e]] = u

        path_taken = [target_id]
        vertex = self.vertices[target_id]
        while vertex is not self.vertices[start_id]:
            vertex = path[vertex]
            path_taken.append(vertex.id)
        path_taken.reverse()

        distance = d[self.vertices[target_id]]
        return path_taken, distance


class AStarPriorityQueue:
    """
    Priority Queue built upon heapq module with support for priority key updates
    Created by Andrew McDonald
    Inspired by https://docs.python.org/2/library/heapq.html
    """

    __slots__ = ['data', 'locator', 'counter']

    def __init__(self) -> None:
        """
        Construct an AStarPriorityQueue object
        """
        self.data = []  # underlying data list of priority queue
        self.locator = {}  # dictionary to locate vertices within priority queue
        self.counter = itertools.count()  # used to break ties in prioritization

    def __repr__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        lst = [f"[{priority}, {vertex}], " if vertex is not None else "" for
               priority, count, vertex in self.data]
        return "".join(lst)[:-1]

    def __str__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        return repr(self)

    def empty(self) -> bool:
        """
        Determine whether priority queue is empty
        :return: True if queue is empty, else false
        """
        return len(self.data) == 0

    def push(self, priority: float, vertex: Vertex) -> None:
        """
        Push a vertex onto the priority queue with a given priority
        :param priority: priority key upon which to order vertex
        :param vertex: Vertex object to be stored in the priority queue
        :return: None
        """
        # list is stored by reference, so updating will update all refs
        node = [priority, next(self.counter), vertex]
        self.locator[vertex.id] = node
        heapq.heappush(self.data, node)

    def pop(self) -> Tuple[float, Vertex]:
        """
        Remove and return the (priority, vertex) tuple with lowest priority key
        :return: (priority, vertex) tuple where priority is key,
        and vertex is Vertex object stored in priority queue
        """
        vertex = None
        while vertex is None:
            # keep popping until we have valid entry
            priority, count, vertex = heapq.heappop(self.data)
        del self.locator[vertex.id]  # remove from locator dict
        vertex.visited = True  # indicate that this vertex was visited
        while len(self.data) > 0 and self.data[0][2] is None:
            heapq.heappop(self.data)  # delete trailing Nones
        return priority, vertex

    def update(self, new_priority: float, vertex: Vertex) -> None:
        """
        Update given Vertex object in the priority queue to have new priority
        :param new_priority: new priority on which to order vertex
        :param vertex: Vertex object for which priority is to be updated
        :return: None
        """
        node = self.locator.pop(vertex.id)  # delete from dictionary
        node[-1] = None  # invalidate old node
        self.push(new_priority, vertex)  # push new node
