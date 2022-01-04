"""
Project 6
CSE 331 S21 (Onsay)
Your Name
hashtable.py
"""

from typing import TypeVar, List, Tuple

T = TypeVar("T")
HashNode = TypeVar("HashNode")
HashTable = TypeVar("HashTable")


class HashNode:
    """
    DO NOT EDIT
    """
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key: str, value: T, deleted: bool = False) -> None:
        self.key = key
        self.value = value
        self.deleted = deleted

    def __str__(self) -> str:
        return f"HashNode({self.key}, {self.value})"

    __repr__ = __str__

    def __eq__(self, other: HashNode) -> bool:
        return self.key == other.key and self.value == other.value

    def __iadd__(self, other: T) -> None:
        self.value += other


class HashTable:
    """
    Hash Table Class
    """
    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity: int = 8) -> None:
        """
        DO NOT EDIT
        Initializes hash table
        :param capacity: capacity of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other: HashTable) -> bool:
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __str__(self) -> str:
        """
        DO NOT EDIT
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    __repr__ = __str__

    def _hash_1(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a bin number for our hash table
        :param key: key to be hashed
        :return: bin number to insert hash item at in our table, None if key is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a hash
        :param key: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    def __len__(self) -> int:
        """
        Getter for the size (that, is, the number of elements) in
        the HashTable

        :returns: int that is size of hash table
        """
        return self.size

    def __setitem__(self, key: str, value: T) -> None:
        """
        Sets the value with an associated key in the HashTable

        :param key: The key we are hashing
        :param value: The associated value we are storing
        :param return: None
        """
        return self._insert(key, value)

    def __getitem__(self, key: str) -> T:
        """
        Looks up the value with an associated key in the HashTable.

        :param key: The key we are searching for the associated value of
        :return: The value with an associated Key
        """
        if self._get(key) is None:
            raise KeyError
        return self._get(key).value

    def __delitem__(self, key: str) -> None:
        """
        Deletes the value with an associated key in the HashTable

        :param key: The key we are deleting the associated value of
        :return: None
        """
        if self._get(key) is None:
            raise KeyError
        return self._delete(key)

    def __contains__(self, key: str) -> bool:
        """
        Determines if a node with the key denoted by the parameter
        exists in the table.

        :param key: the key we are checking to be part of Hash Table
        :return: True if key is present, otherwise False
        """
        if self._get(key) is not None:
            return True
        return False

    def hash(self, key: str, inserting: bool = False) -> int:
        """
        Given a key string return an index in the hash table.

        :param key: the key being used in our hash
        :param inserting: True if inserting, otherwise False
        :return: the key that is the bin we hashed into
        """
        apple = self._hash_1(key)
        mango = self._hash_2(key)
        # ultimately return index and use in insert
        if self.table[apple] is None:
            return apple

        for i in range(len(self.table)):
            grapes = (apple + (i * mango)) % len(self.table)
            if grapes is None:
                return grapes
            if self.table[grapes] is None or self.table[grapes].deleted and \
                    inserting or self.table[grapes].key == key:
                break
            i + 1
        return grapes

    def _insert(self, key: str, value: T) -> None:
        """
        Use the key and value parameters to add a HashNode to the hash table.
        If the key exists, overwrite the existing value

        :param key: the key associated with the value we are storing
        :param value: the associated value we are storing
        :return: None
        """
        index = self.hash(key, inserting=True)
        hash_node = self.table[index]

        if hash_node:
            if hash_node.key == key:
                hash_node.value = value
                return None

        self.table[index] = HashNode(key, value)
        self.size += 1

        if self.size >= self.capacity / 2:
            self._grow()

        return None

    def _get(self, key: str) -> HashNode:
        """
        Find the HashNode with the given key in the hash table.

        :param key: the key we are looking up.
        :return: Hashnode with the key looked into.
        """
        index = self.hash(key)
        if index is None:
            return None
        return self.table[index]

    def _delete(self, key: str) -> None:
        """
        Removes the HashNode with the given key from the hash table .
        If the node is found assign its key and value to None, and
        set the deleted flag to True

        :param key: the key of the node we are looking into to delete
        :return: None
        """
        index = self.hash(key)
        hash_node = self.table[index]

        if hash_node:
            if hash_node.key == key:
                hash_node.key, hash_node.value = None, None
                hash_node.deleted = True
                self.size -= 1

        return None

    def _grow(self) -> None:
        """
        Double the capacity of the existing hash table.

        :return: None
        """

        self.capacity *= 2
        new_hash = HashTable(self.capacity)
        self.prime_index = new_hash.prime_index

        index = 0
        while index < (self.capacity / 2):
            node = self.table[index]
            if node:
                if not node.deleted:
                    new_hash._insert(node.key, node.value)
            index += 1

        self.table = new_hash.table

        return None

    def update(self, pairs: List[Tuple[str, T]] = []) -> None:
        """
        Updates the hash table using an iterable of key value pairs
        If the value already exists, update it, otherwise enter it
        into the table.

        :param pairs:  list of tuples (key, value) being updated
        :return: None
        """
        for i in range(len(pairs)):
            self[pairs[i][0]] = pairs[i][1]

    def keys(self) -> List[str]:
        """
        Makes a list that contains all of the keys in the table

        :return: list of the keys
        """
        some_list = []
        for i in self.table:
            if i is None:
                continue
            some_list.append(i.key)
        return some_list

    def values(self) -> List[T]:
        """
        Makes a list that contains all of the values in the table.

        :return: list of the values
        """
        some_list = []
        for i in self.table:
            if i is None:
                continue
            if i.value is not None:
                some_list.append(i.value)
        return some_list

    def items(self) -> List[Tuple[str, T]]:
        """
        Makes a list that contains all of the keys in the table.

        :return: list of the tuples of the form.
        """
        some_list = []
        for i in self.table:
            if i is None:
                continue
            if i.value is not None:
                some_list.append((i.key, i.value))
        return some_list

    def clear(self) -> None:
        """
        Should clear the table of HashNodes completely, in essence a reset of the table

        :param: None
        """
        self.size = 0
        self.table = [None] * self.capacity


class CataData:
    def __init__(self) -> None:
        """
        Initializes the CataData.
        """
        self.cata_data = HashTable()

    def enter(self, idx: str, origin: str, time: int) -> None:
        """
        This function records the entry time when a rider hops onto to
        ride a bus.

        :param idx: the ID of the person
        :param origin: the origin station
        :param time: the entry time
        :return: None
        """
        self.cata_data[idx] = (origin, time)

    def exit(self, idx: str, dest: str, time: int) -> None:
        """
        This function records the exit time when a rider hops out of the
        bus.

        :param idx: the ID of the person.
        :param dest: the destination station
        :param time: the exit time
        :return: None
        """
        data = self.cata_data[idx]
        del self.cata_data[idx]
        new_key = str(data[0] + "-" + dest)
        if new_key in self.cata_data:
            average_table_data = self.cata_data[new_key]
            new_time = average_table_data[0] + time - data[1]
            # number_of_trips = average_table_data[1] + 1
            self.cata_data[new_key] = (new_time, average_table_data[1] + 1)
        else:
            self.cata_data[new_key] = (time - data[1], 1)

    def get_average(self, origin: str, dest: str) -> float:
        """
        Gets the average travel time of users riding CATA busses from origin to
        dest.

        :param origin: the origin station
        :param dest: the destination station
        :return: the average time
        """
        key = str(origin + "-" + dest)
        if key in self.cata_data:
            average_time = float(self.cata_data[key][0] / self.cata_data[key][1])
            return average_time

        return float(0)
