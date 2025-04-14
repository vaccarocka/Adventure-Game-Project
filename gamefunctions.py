#Saige Vacca
#CSCI 150.50
#4.13.2025
#Assignment 12



"""This module contains functions for my simple text-based game, including a
vegetarian shop system and random monster generation. Functions include
printing a welcome messages, displaying a veggie-friendly shop menu, handling
item purchases, and creating random monsters!
"""

import random
import json
from pathlib import Path
import pygame

def main_menu():
    """Start up game menu with introduction. Allows player to choose new game
    file or continue save file."""
    print("\n\n\nWelcome to Saige's Adventure Game Project!")
    print("\n\n\nType 1 to start new game or type 2 to load save file.")
    game_select = input()
    if game_select == "1":
        return "start_new_game"
    elif game_select == "2":
        return "load_save_file"

def load_game():
    """Opens up JSON file, splits JSON data into individual variables then
    returns those variables."""
    save_file_path = Path.cwd().joinpath("save_file.json")
    with save_file_path.open("r") as file:
        game_data = json.load(file)
    player_name = game_data["name"]
    curr_HP = game_data["hp"]
    curr_gold = game_data["gold"]
    curr_inventory = game_data["inventory"]
    curr_equipped = game_data["equipped"]
    map_positions = game_data["map"]
    return (player_name, curr_HP, curr_gold, curr_inventory, curr_equipped, map_positions)

def save_game(player_name, curr_HP, curr_gold, curr_inventory, curr_equipped, map_positions):
    """Combines player variables into one dictionary then saves that dictionary
    as a JSON file for later retrieval."""
    game_data = {
        "name": player_name,
        "hp": curr_HP,
        "gold": curr_gold,
        "inventory": curr_inventory,
        "equipped": curr_equipped,
        "map": map_positions
    }
    save_file_path = Path.cwd().joinpath("save_file.json")
    with save_file_path.open("w") as file:
        json.dump(game_data, file, indent = 4)
    print("Game save successful. Goodbye!")
    input("Press Enter to continue")

def print_welcome(name: str, width: int = 20) -> None:
    """Print a centered welcome message within the specified width.
    Parameters: name (str): The name of the player. width (int, optional):
    The width of the message formatting. Defaults to 20. Returns: None"""
    message = f"Hello, {name}!!"
    print(f"\n\n\n{message:^{width}}")

def status_message(curr_HP, curr_gold):
    """Welcome the player with setting and current player status."""
    print("\n\n\nYou wake up in a quiet and secluded forest town.")
    print(f"Current HP: {curr_HP}, Current Gold: {curr_gold}")
    print("What would you like to do?")

def combat_function(monster_start_HP, curr_HP, curr_equipped):
    """Display and run turn based combat between player and monster. Returns
    player and monster HP values post-battle."""
    monst_damage_pl = random.randint(2,7)
    if curr_equipped["shield"]["name"].lower() == "buckler":
        monst_damage_pl -= random.randint(3,8)
        if monst_damage_pl <= 0:
            monst_damage_pl = 0
            print("The monster tried to claw at you, but your shield negated all damage!")
        else:
            print(f"The monster attacked, but the shield reduced damage to just {monst_damage_pl}. Phew!")
        curr_equipped["shield"]["uses"] -= 1
        if curr_equipped["shield"]["uses"] < 1:
            curr_equipped["shield"] = {"name": "none"}
            print("Your shield snaps in half!!!")
    else:
        print(f"You take a blow! Damage dealt by monster: {monst_damage_pl}!")
    curr_HP = curr_HP - monst_damage_pl
    player_damage_monst = random.randint(1,15)
    if curr_equipped["weapon"]["name"].lower() == "sword":
        player_damage_monst += 10
        print(f"You draw your weapon and swing! You land a blow. Damage dealt by player: {player_damage_monst}!")
        curr_equipped["weapon"]["uses"] -= 1
        if curr_equipped["weapon"]["uses"] < 1:
            curr_equipped["weapon"] = {"name": "none"}
            print("Your sword snaps in half!!!")
    else:
        print(f"You karate chop the monster! Damage dealt by player: {player_damage_monst}!")

    monster_start_HP = monster_start_HP - player_damage_monst
    return (monster_start_HP, curr_HP, curr_equipped)

def monster_fight(curr_HP, curr_gold, curr_equipped, monster_position):
    """Introduces monster and runs combat loop, prompting player to fight to the
    death or flee. Returns player HP and gold."""
    print("\n\n\nYou hear footsteps behind you. You turn around and see ... a monster! It lunges towards you.")
    monster_start_HP = 40
    while curr_HP > 0 and monster_start_HP > 0:
        print("\n\n\n")
        if curr_equipped["weapon"]["name"].lower() == "sword":
            print(f"You currently have a Sword equipped.  It increases your damage by 10, and has {curr_equipped["weapon"]["uses"]} uses left.")
        if curr_equipped["shield"]["name"].lower() == "buckler":
            print(f"You currently have a Buckler equipped.  It reduces your damage by a number from 3 to 8, and has {curr_equipped["shield"]["uses"]} uses left.")
        fight_options = "1) Fight!\n2) Flee!\n"
        if curr_equipped["special item"]["name"].lower() == "shiny ring":
            print(f"You currently have a Shiny Ring equipped.  It has {curr_equipped["special item"]["uses"]} uses left.")
            fight_options += "3) Befriend monster using the Shiny Ring"
        print(f"Player Current HP: {curr_HP}, Monster Current HP: {monster_start_HP}")
        Fight_selection = input(fight_options + "\n")
        if Fight_selection == "1":
            monster_start_HP, curr_HP, curr_equipped = combat_function(monster_start_HP, curr_HP, curr_equipped)
        elif Fight_selection == "2":
            break
        elif Fight_selection == "3" and curr_equipped["special item"]["name"].lower() == "shiny ring":
            print("You reveal the Shiny Ring, and the monster says, \"I've been looking for this! Thanks you so very much!\" and they run back into the forest (leaving behind a pile of gold coins).")
            curr_equipped["special item"] = {"name": "none"}
            monster_start_HP = 0
        else:
            print("Try again Nerd!")
    if monster_start_HP < 1 and curr_HP > 0:
        winner_gold = random.randint(1,10)
        curr_gold = curr_gold + winner_gold
        monster_position = [random.randint(6,9), random.randint(0,9)]

        print(f"You defeat the monster. You find {winner_gold} Gold!")
        input("Press Enter to continue.")
    return curr_HP, curr_gold, curr_equipped, monster_position

def playersleep(curr_HP, player_gold):
    """Introduces sleep option to player. Subtracts gold for gained HP. Returns
    player HP and gold."""
    print("\n\n\nYou follow a beaten path to a clearing that reveals an Inn. It seems tattered and rickety, but the aroma of fresh bread and the promise of soft pillows draw you in.")
    print("You encounter the Innkeeper. They take 5 Gold from you and point you towards your room for the night.")
    player_gold = player_gold - 5
    curr_HP = curr_HP + 10
    input("Press Enter to continue.")
    return (curr_HP, player_gold)

def display_items(item_list, detail_list=[]):
    """Takes a list of item dictionaries and prints out their name and
    description. Allows to optionally print out other details about each item,
    including uses left, price, and item type."""
    item_strings = []
    if item_list == []:
        return "\nnothing\n"

    for item in item_list:
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

def get_item_names(item_list):
    """Takes a list of item dictionaries and returns a list of the name values."""
    item_names = []
    for item in item_list:
        item_names.append(item["name"].lower())
    return item_names

def get_item_by_name(item_list, name):
    """Takes a list of item dictionaries and returns the dictionary that has a
    matching name value."""
    for item in item_list:
        if item["name"].lower() == name.lower():
            return item

def get_items_by_type(item_list, type):
    """Takes a list of item dictionaries and returns a new list with items of
    matching types."""
    new_item_list = []
    for item in item_list:
        if item["type"] == type:
            new_item_list.append(item)
    return new_item_list

def remove_item_by_name(item_list, name):
    """Takes a list of item dictionaries and removes dictionary with matching
    name value"""
    for i in range(len(item_list)):
        if item_list[i]["name"].lower() == name.lower():
            item_list.pop(i)
            return item_list

def purchase_item(player_gold, curr_inventory, item):
    """Subtracts item price from player gold when purchased. Adds the item to
    the players inventory. Prints message if player does not have enough Gold
    to purchase item."""
    if player_gold >= item["price"]:
        player_gold -= item["price"]
        curr_inventory.append(item)
    else:
        print(f"Sorry, {item["name"]} costs {item["price"]}, but you only have {player_gold} gold.")
    return player_gold, curr_inventory

def shop_menu(player_gold, curr_inventory, shop_items):
    """Welcomes player to the item shop and lists shop inventory. Prompts user to buy
    items."""
    print("\n\n\nYou enter the shop and are greeted by the shopkeep")
    while True:
        print(f"\n\n\nCurrent gold: {player_gold}\nYour current inventory: {display_items(curr_inventory)}")
        print(f"\nShop inventory: {display_items(shop_items, ["type", "price"])}")
        shop_select = input("Type the name of the item you would like to buy, or 'Q' to quit\n")
        if shop_select.lower() == "q":
            return player_gold, curr_inventory
        elif shop_select.lower() in get_item_names(shop_items):
            for item in shop_items:
                if item["name"].lower() == shop_select.lower():
                    player_gold, curr_inventory = purchase_item(player_gold, curr_inventory, item)
                    break
        else:
            print(f"Sorry, I don't know what a {shop_select} is.")

def equip_item(curr_equipped, curr_inventory, type):
    """Switches items between player equipment and item inventory."""
    if curr_equipped[type]["name"] != "none":
        curr_inventory.append(curr_equipped[type])
    print(f"\nWhich item to equip as {type}? {display_items(get_items_by_type(curr_inventory, type))}")
    while True:
        equip_select = input("Type the name of the item you would like to equip.\n")
        if equip_select.lower() in get_item_names(get_items_by_type(curr_inventory, type)):
            for item in curr_inventory:
                if item["name"].lower() == equip_select.lower():
                    curr_equipped[type] = item
                    curr_inventory = remove_item_by_name(curr_inventory, item["name"])
                    return curr_equipped, curr_inventory
        else:
            print("Sorry, you didn't enter the name of an item.")

def inventory_menu(curr_equipped, curr_inventory):
    """Displays player equipped items and player inventory items. Prompts player to equip
    by item type."""
    while True:
        print(f"\n\n\nYour current inventory: {display_items(curr_inventory, ["type", "uses"])}")
        print(f"Currently equipped items:\nWeapon: {curr_equipped["weapon"]["name"]}\nShield: {curr_equipped["shield"]["name"]}\nSpecial Item: {curr_equipped["special item"]["name"]}")
        inventory_select = input("Type 'Weapon', 'Shield', or 'Special Item' to change equipment.  Type 'Q' to quit.").lower()
        if inventory_select == "q":
            return curr_equipped, curr_inventory
        elif inventory_select == "weapon" or inventory_select == "shield" or inventory_select == "special item":
            curr_equipped, curr_inventory = equip_item(curr_equipped, curr_inventory, inventory_select)
        else:
            print(f"Sorry, I don't recognize equipment type: {inventory_select}")

    return equipment, inventory


def traverse_map(map_positions):
    """
    Draws a map made up of 32 pixel tiles, and allows the user to move the character with the arrow keys. Returns map positions and what the next action should be.  """
    pygame.init()
    tile_size = 32
    screen = pygame.display.set_mode((tile_size * 10, tile_size * 10))
    clock = pygame.time.Clock()

    moved = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return map_positions, "quit game"
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_UP and map_positions["player_position"][1] > 0:
                map_positions["player_position"][1] -= 1
                moved = True
            elif event.key == pygame.K_DOWN and map_positions["player_position"][1] < 9:
                map_positions["player_position"][1] += 1
                moved = True
            elif event.key == pygame.K_LEFT and map_positions["player_position"][0] > 0:
                map_positions["player_position"][0] -= 1
                moved = True
            elif event.key == pygame.K_RIGHT and map_positions["player_position"][0] < 9:
                map_positions["player_position"][0] += 1
                moved = True

        screen.fill("antiquewhite2")
        pygame.draw.rect(screen, "aquamarine3", pygame.Rect(map_positions["player_position"][0] * tile_size, map_positions["player_position"][1] * tile_size, 32, 32))
        pygame.draw.circle(screen, "green", ((map_positions["town_position"][0] * tile_size) + (tile_size / 2), (map_positions["town_position"][1] * tile_size) + (tile_size / 2)), 16)
        pygame.draw.circle(screen, "red", ((map_positions["monster_position"][0] * tile_size) + (tile_size / 2), (map_positions["monster_position"][1] * tile_size) + (tile_size / 2)), 16)
        pygame.display.flip()
        clock.tick(30)

        if not moved:
            continue
        elif map_positions["player_position"] == map_positions["town_position"]:
            next_action = "town menu"
            break
        elif map_positions["player_position"] == map_positions["monster_position"]:
            next_action = "fight monster"
            break

    pygame.quit()
    return map_positions, next_action
