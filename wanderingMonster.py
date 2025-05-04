#Saige Vacca
#CSCI 150.50
#4.27.2025
#Assignment 14

import random

class Monster:
    """Class that defines Monster objects that keep track of various properties of a monster, as well as provide movement and data conversion for save/load game functionality."""
    def __init__(self, from_dictionary = None):
        """Initialize a monster object, either with values provided by a dictionary (from loading the game) or by randomizing one using the values and value ranges in the monster table."""
        if from_dictionary:
            self.type = from_dictionary["type"]
            self.hp = from_dictionary["hp"]
            self.gold = from_dictionary["gold"]
            self.damage_range = from_dictionary["damage_range"]
            self.color = from_dictionary["color"]
            self.position = from_dictionary["position"]
            self.alive = from_dictionary["alive"]
        else:
            monster_table = [
                {"type": "slime", "color": "violet", "damage_range": (1, 7), "hp_range": (10, 20), "gold_range": (4, 7)},
                {"type": "wyrm", "color": "darkred", "damage_range": (5, 10), "hp_range": (15, 30), "gold_range": (10, 17)},
                {"type": "ogre", "color": "olivedrab", "damage_range": (8, 15), "hp_range": (26, 38), "gold_range": (15, 25)},
                {"type": "lich", "color": "gray45", "damage_range": (12, 25), "hp_range": (30, 49), "gold_range": (30, 45)}
            ]

            random_monster = random.choice(monster_table)
            self.type = random_monster["type"]
            self.hp = random.randint(*random_monster["hp_range"])
            self.gold = random.randint(*random_monster["gold_range"])
            self.damage_range = random_monster["damage_range"]
            self.color = random_monster["color"]
            self.position = [random.randint(6,9), random.randint(0,9)]
            self.alive = True

    def move(self, town_position, board_size=(10,10)):
        """Moves the monster's position in a random cardinal direction.  Retries if it happens to select the same position as the town, or a space outside of the board's tile boundary."""
        if not self.alive:
            return
        moved = False
        while moved == False:
            potential_move = self.position.copy()
            direction = random.choice(["up", "down", "left", "right"])

            if direction == "left":
                potential_move[0] -= 1
            elif direction == "right":
                potential_move[0] += 1
            if direction == "up":
                potential_move[1] -= 1
            elif direction == "down":
                potential_move[1] += 1

            if potential_move == town_position:
                continue
            elif (potential_move[0] < 0 or potential_move[0] >= board_size[0]) or (potential_move[1] < 0 or potential_move[1] >= board_size[1]):
                continue
            else:
                self.position = potential_move.copy()
                moved = True

    def get_dictionary(self):
        """returns a dictionary containing all the properties of the monster.  This allows passing data to the json module for saving, as json.dump() doesn't support instances of objects."""
        return {
            "type": self.type,
            "hp": self.hp,
            "gold": self.gold,
            "damage_range": self.damage_range,
            "color": self.color,
            "position": self.position,
            "alive": self.alive
        }
