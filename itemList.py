#Saige Vacca
#CSCI 150.50
#5.4.2025
#Assignment 15

import random
import uuid

class itemList():
    """Class that includes a list of item dictionaries, as well as methods for modifying and displaying the list."""
    def __init__(self, items = []):
        self.list = items
        for item in self.list:
            if "uuid" not in item.keys():
                item["uuid"] = str(uuid.uuid4())

    def append(self, item):
        if "uuid" not in item.keys():
            item["uuid"] = str(uuid.uuid4())
        self.list.append(item)

    def display(self, detail_list=[]):
        """Takes a list of item dictionaries and prints out their name and
        description. Allows to optionally print out other details about each item,
        including uses left, price, and item type."""
        item_strings = []
        if self.list == []:
            return "\nnothing\n"

        for item in self.list:
            new_item_string = f"\n{item["name"]}: {item["description"]}"
            for detail in detail_list:
                if detail not in item.keys():
                    pass
                elif detail == "type":
                    new_item_string += f"\n    Type: {item["type"]}"
                elif detail == "price":
                    new_item_string += f"\n    Price: {item["price"]} gold"
                elif detail == "uses":
                    new_item_string += f"\n    Uses left: {item["uses"]}"
            item_strings.append(new_item_string)
        return "".join(item_strings) + "\n"

    def item_names(self):
        """Takes a list of item dictionaries and returns a list of the name values."""
        names = []
        for item in self.list:
            names.append(item["name"].lower())
        return names

    def get_items(self, name = None, type = None):
        """Takes a list of item dictionaries and returns the dictionary that has a
        matching name value."""
        new_item_list = []
        if name:
            for item in self.list:
                if item["name"].lower() == name.lower():
                    new_item_list.append(item)
        elif type:
            for item in self.list:
                if item["type"] == type:
                    new_item_list.append(item)
        return new_item_list


    def remove_item(self, item):
        """Takes a list of item dictionaries and removes dictionary with matching
        uuid"""
        for i in range(len(self.list)):
            if self.list[i]["uuid"] == item["uuid"]:
                self.list.pop(i)
                return
