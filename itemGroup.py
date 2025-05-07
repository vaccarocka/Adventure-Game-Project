#Saige Vacca
#CSCI 150.50
#5.4.2025
#Assignment 15

import pygame
from pathlib import Path

class itemGroup:
    """Class that holds a list of grid squares and attributes of the grid spaces for pygame to be able to draw the player's items in a GUI."""
    def __init__(self, item_grid_start, item_type, group_size = 11, is_equipment_slot = False):
        self.grid_size = (61, 61)
        self.grid_offset = 70
        self.group = []
        self.item_grid_start = item_grid_start
        self.type = item_type
        self.is_equipment_slot = is_equipment_slot

        x_pos = self.item_grid_start[0]
        y_pos = self.item_grid_start[1]
        for i in range(group_size):
            """This loop generates a list of grid spaces, each represented as a dictionary with the item data, a png image, and the rectangular coordinates they should be drawn at."""
            self.group.append({"item": None, "image": None, "rect": pygame.Rect((x_pos, y_pos), (self.grid_size))})
            x_pos += self.grid_offset
            if i == 5:
                y_pos += self.grid_offset
                x_pos = item_grid_start[0]

    def update(self, items):
        """clears the item data and image data for every grid square, then assigns each of the passed items in the list argument to one of the grid squares.  Lastly, loads the
        png with the same name as the item's name."""
        for grid in self.group:
            grid["item"] = None
            grid["image"] = None

        for i in range(len(items)):
            self.group[i]["item"] = items[i]

        for grid in self.group:
            if grid["item"]:
                grid["image"] = pygame.image.load(Path.cwd().joinpath("sprites", "items", f"{grid["item"]["name"].lower()}.png")).convert()
                pygame.transform.scale(grid["image"], self.grid_size)

    def is_item_in_group(self, item_to_check):
        """references the uuid of the passed item to check if it already is represented in a grid square of this group."""
        for grid in self.group:
            if not grid["item"]:
                continue
            elif grid["item"]["uuid"] == item_to_check["uuid"]:
                return True
        return False
