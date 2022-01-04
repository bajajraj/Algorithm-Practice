"""
Rajaditya Shrikishan Bajaj
Coding Challenge 8
CSE 331 Spring 2021
Professor Sebnem Onsay
"""

from typing import Set, Tuple, Dict
from CC8.InventoryItems import ItemInfo, ALL_ITEMS


def changed_number(stack_amount: int, amount: int) -> float:
    """
    It changes the given amount in a fraction so that we can easily
    store the total amount.

    :param stack_amount: the given stack amount
    :param amount: the given amount
    :return: the converted amount.
    """
    if stack_amount == 64:
        changed_amount = float(amount / stack_amount)
    elif stack_amount == 16:
        new_amount = amount * 4
        stack_amount *= 4
        changed_amount = float(new_amount / stack_amount)
    elif stack_amount == 1:
        new_amount = amount = 64
        stack_amount *= 64
        changed_amount = float(new_amount / stack_amount)
    return changed_amount


class Bundle:
    """ Bundle Class """

    def __init__(self) -> None:
        """
        Creates an instance of Bundle
        """
        self.bundle_dict = {}
        self.total_items = 0.0

    def to_set(self) -> Set[Tuple[str, int]]:
        """
        Converts the bundle to a set of tuples

        :return: a set where of tuples where first element is
                 item and second is the amount
        """
        bundle_set = set()
        for key in self.bundle_dict:
            bundle_set.add((key, self.bundle_dict[key]))
        return bundle_set

    def add_to_bundle(self, item_name: str, amount: int) -> bool:
        """
        Adds an amount of an item to the bundle if possible

        :param item_name: the name of the item to be added to the bundle
        :param amount: the amount of the itemName to be added to the bundle
        :return: a bool representing whether the add to the bundle was successful,
        """
        item_info = ALL_ITEMS.items[item_name]
        stack_amount = item_info.amount_in_stack
        fraction_amount = changed_number(stack_amount, amount)
        total = self.total_items
        total += fraction_amount
        if total > 1:
            return False
        if item_name in self.bundle_dict:
            self.bundle_dict[item_name] += amount
        else:
            self.bundle_dict[item_name] = amount
        self.total_items += fraction_amount
        return True

    def remove_from_bundle(self, item_name: str, amount: int) -> bool:
        """
        Removes an amount of an item from the bundle if possible

        :param item_name: the name of the item to be removed from the bundle
        :param amount: int: the amount of the itemName to be removed from the bundle
        :Return: a bool representing whether the remove operation was successful
        """
        item_info = ALL_ITEMS.items[item_name]
        stack_amount = item_info.amount_in_stack
        fraction_amount = changed_number(stack_amount, amount)
        if item_name in self.bundle_dict:
            amount_dict = self.bundle_dict[item_name]
            if amount_dict >= amount:
                self.total_items -= fraction_amount
                new_amount = amount_dict - amount
                if new_amount == 0:
                    del self.bundle_dict[item_name]
                else:
                    self.bundle_dict[item_name] = new_amount
                return True
            return False
        return False
