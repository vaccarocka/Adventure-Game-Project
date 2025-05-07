#Saige Vacca
#CSCI 150.50
#5.4.2025
#Assignment 15



"""This module contains functions for my simple text-based game, including a
vegetarian shop system and random monster generation. Functions include
printing a welcome messages, displaying a veggie-friendly shop menu, handling
item purchases, and creating random monsters!
"""

import random
import json
from pathlib import Path
import pygame
import wanderingMonster
from itemGroup import itemGroup
from itemList import itemList

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

def load_game(player, map_data):
    """Opens up JSON file, splits JSON data into individual variables then
    returns those variables."""
    save_file_path = Path.cwd().joinpath("save_file.json")
    with save_file_path.open("r") as file:
        game_data = json.load(file)
    player.update(game_data["player"])
    player["inventory"] = itemList(game_data["inventory"])
    map_data.update(game_data["map_data"])
    map_data["monster 1"] = wanderingMonster.Monster(game_data["monster 1"])
    map_data["monster 2"] = wanderingMonster.Monster(game_data["monster 2"])

def save_game(player, map_data):
    """Combines player variables into one dictionary then saves that dictionary
    as a JSON file for later retrieval."""
    monster_1 = map_data.pop("monster 1")
    monster_2 = map_data.pop("monster 2")
    inventory = player.pop("inventory").list
    game_data = {
        "player": player,
        "inventory": inventory,
        "map_data": map_data,
        "monster 1": monster_1.get_dictionary(),
        "monster 2": monster_2.get_dictionary()
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

def status_message(player):
    """Welcome the player with setting and current player status."""
    print("\n\n\nYou wake up in a quiet and secluded forest town.")
    print(f"Current HP: {player["HP"]}, Current Gold: {player["gold"]}")
    print("What would you like to do?")

def combat_function(player, monster):
    """Display and run turn based combat between player and monster. Returns
    player and monster HP values post-battle."""
    monst_damage_pl = random.randint(*monster.damage_range)
    if player["equipped"]["shield"]:
        monst_damage_pl -= random.randint(*player["equipped"]["shield"]["block range"])
        if monst_damage_pl <= 0:
            monst_damage_pl = 0
            print(f"The {monster.type} tried to claw at you, but your {player["equipped"]["shield"]["name"]} negated all damage!")
        else:
            print(f"The {monster.type} attacked, but your {player["equipped"]["shield"]["name"]} reduced damage to just {monst_damage_pl}. Phew!")
        player["equipped"]["shield"]["uses"] -= 1
        if player["equipped"]["shield"]["uses"] < 1:
            player["equipped"]["shield"] = None
            print("Your shield snaps in half!!!")
    else:
        print(f"You take a blow! Damage dealt by {monster.type}: {monst_damage_pl}!")
    player["HP"] -= monst_damage_pl
    player_damage_monst = random.randint(1,15)
    if player["equipped"]["weapon"]:
        player_damage_monst += player["equipped"]["weapon"]["damage increase"]
        print(f"You draw your weapon and swing! You land a blow. Damage dealt by player: {player_damage_monst}!")
        player["equipped"]["weapon"]["uses"] -= 1
        if player["equipped"]["weapon"]["uses"] < 1:
            player["equipped"]["weapon"] = None
            print("Your sword snaps in half!!!")
    else:
        print(f"You karate chop the {monster.type}! Damage dealt by player: {player_damage_monst}!")

    monster.hp -= player_damage_monst
    return

def monster_fight(player, monster):
    """Introduces monster and runs combat loop, prompting player to fight to the
    death or flee. Returns player HP and gold."""
    print(f"\n\n\nYou hear footsteps behind you. You turn around and see ... a {monster.type}! It lunges towards you.")
    while player["HP"] > 0 and monster.hp > 0:
        print("\n\n\n")
        if player["equipped"]["weapon"]:
            print(f"You currently have a {player["equipped"]["weapon"]["name"]} equipped.  It {player["equipped"]["weapon"]["description"]}, and has {player["equipped"]["weapon"]["uses"]} uses left.")
        if player["equipped"]["shield"]:
            print(f"You currently have a {player["equipped"]["shield"]["name"]} equipped.  It {player["equipped"]["shield"]["description"]}, and has {player["equipped"]["shield"]["uses"]} uses left.")
        fight_options = "1) Fight!\n2) Flee!\n"
        if player["equipped"]["special item"]:
            print(f"You currently have a Shiny Ring equipped.  It has {player["equipped"]["special item"]["uses"]} uses left.")
            fight_options += f"3) Befriend {monster.type} using the Shiny Ring"
        print(f"Player Current HP: {player["HP"]}, {monster.type.title()} Current HP: {monster.hp}")
        Fight_selection = input(fight_options + "\n")
        if Fight_selection == "1":
            combat_function(player, monster)
        elif Fight_selection == "2":
            break
        elif Fight_selection == "3" and player["equipped"]["special item"]:
            print(f"You reveal the Shiny Ring, and the {monster.type} says, \"I've been looking for this! Thanks you so very much!\" and they run back into the forest (leaving behind a pile of gold coins).")
            player["equipped"]["special item"] = None
            monster.hp = 0
        else:
            print("Try again Nerd!")
    if monster.hp < 1 and player["HP"] > 0:
        player["gold"] += monster.gold
        monster.position = [-1, -1]
        monster.alive = False

        print(f"You defeat the monster. You find {monster.gold} Gold!")
        input("Press Enter to continue.")

def playersleep(player):
    """Introduces sleep option to player. Subtracts gold for gained HP. Returns
    player HP and gold."""
    print("\n\n\nYou follow a beaten path to a clearing that reveals an Inn. It seems tattered and rickety, but the aroma of fresh bread and the promise of soft pillows draw you in.")
    print("You encounter the Innkeeper. They take 5 Gold from you and point you towards your room for the night.")
    player["gold"] -= 5
    player["HP"] += 10
    input("Press Enter to continue.")



def purchase_item(player, item):
    """Subtracts item price from player gold when purchased. Adds the item to
    the players inventory. Prints message if player does not have enough Gold
    to purchase item."""
    if player["gold"] >= item["price"]:
        player["gold"] -= item["price"]
        player["inventory"].append(item)
    else:
        print(f"Sorry, {item["name"]} costs {item["price"]}, but you only have {player["gold"]} gold.")

def shop_menu(player, shop_items):
    """Welcomes player to the item shop and lists shop inventory. Prompts user to buy
    items."""
    print("\n\n\nYou enter the shop and are greeted by the shopkeep")
    while True:
        print(f"\n\n\nCurrent gold: {player["gold"]}\nYour current inventory: {player["inventory"].display()}")
        print(f"\nShop inventory: {shop_items.display(["type", "price"])}")
        shop_select = input("Type the name of the item you would like to buy, or 'Q' to quit\n")
        if shop_select.lower() == "q":
            return
        elif shop_select.lower() in shop_items.item_names():
            for item in shop_items.list:
                if item["name"].lower() == shop_select.lower():
                    purchase_item(player, item)
                    break
        else:
            print(f"Sorry, I don't know what a {shop_select} is.")

def equip_item(player, item):
    """Takes a player dictionary and an item dictionary, removes the item from the player's inventory, adding to their equipment.
    If there is already an item of the same type equipped, move it to inventory before equipping the passed item argument."""
    if player["equipped"][item["type"]]:
        player["inventory"].append(player["equipped"][item["type"]])
    player["equipped"][item["type"]] = item
    player["inventory"].remove_item(item)


def unequip_item(player, item):
    """takes a player dictionary and an item dictionary, removes the item from the player's equipment, adding it to the player inventory."""
    player["inventory"].append(player["equipped"][item["type"]])
    player["equipped"][item["type"]] = None


def inventory_menu(player):
    """Launches graphical menu that displays the player's inventory alongside their equipment slots, and allows equipping and unequipping
    items by clicking and dragging items between the item slots."""
    pygame.init()
    weapon_group = itemGroup((35, 203), "weapon")
    shield_group = itemGroup((35, 403), "shield")
    special_group = itemGroup((35, 603), "special item")
    equipped_weapon = itemGroup((573, 203), "weapon", 1, is_equipment_slot = True)
    equipped_shield = itemGroup((573, 403), "shield", 1, is_equipment_slot = True)
    equipped_special = itemGroup((573, 603), "special item", 1, is_equipment_slot = True)
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    background = pygame.image.load(Path.cwd().joinpath("sprites", "inventory_menu.png")).convert()
    selected = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                """checks if a grid space containing an item is clicked, and if so it is copied into the 'selected' variable"""
                for group in [weapon_group, shield_group, special_group, equipped_weapon, equipped_shield, equipped_special]:
                    for grid in group.group:
                        if not grid["item"]:
                            continue
                        elif grid["rect"].collidepoint(event.pos):
                            selected = grid.copy()
                            selected["rect"] = pygame.Rect((grid["rect"].x, grid["rect"].y), group.grid_size)



            elif event.type == pygame.MOUSEBUTTONUP:
                """checks if the mouse is released on an empty grid space while an item is selected.  Then checks if the item you
                are dropping in the space is compatible, and finally runs either equip_item() or unequip_item() appropriately."""
                for group in [weapon_group, shield_group, special_group, equipped_weapon, equipped_shield, equipped_special]:
                    for grid in group.group:
                        if grid["item"] and not group.is_equipment_slot:
                            continue
                        elif not selected:
                            continue
                        elif grid["rect"].collidepoint(event.pos) and not group.is_item_in_group(selected["item"]):
                            if group.type == selected["item"]["type"] and group.is_equipment_slot:
                                equip_item(player, selected["item"])
                                selected = None
                            elif group.type == selected["item"]["type"] and not group.is_equipment_slot:
                                unequip_item(player, selected["item"])
                                selected = None
                selected = None
            else:
                pass

        """Updates all the grid groups with the current items in inventory and equipment.  This allows the grid
        spaces to update after items are equipped or moved around."""
        weapon_group.update(player["inventory"].get_items(type = "weapon"))
        shield_group.update(player["inventory"].get_items(type = "shield"))
        special_group.update(player["inventory"].get_items(type = "special item"))
        equipped_weapon.update([player["equipped"]["weapon"]])
        equipped_shield.update([player["equipped"]["shield"]])
        equipped_special.update([player["equipped"]["special item"]])

        """First blit the background, then go through all grid spaces in all groups and blit them on top of the background, unless they are the selected item.
        Finally, blit the selected item (if any) to the current position of the mouse cursor."""
        screen.blit(background, (0,0))
        for group in [weapon_group, shield_group, special_group, equipped_weapon, equipped_shield, equipped_special]:
            for grid in group.group:
                if not grid["image"]:
                    continue
                elif not selected:
                    pass
                elif grid["item"]["uuid"] == selected["item"]["uuid"]:
                    continue
                screen.blit(grid["image"], (grid["rect"].x, grid["rect"].y))
        if selected:
            selected["rect"].x = pygame.mouse.get_pos()[0]
            selected["rect"].y = pygame.mouse.get_pos()[1]
            screen.blit(selected["image"], (selected["rect"].x, selected["rect"].y))


        pygame.display.flip()
        clock.tick(30)


def traverse_map(map_data):
    """
    Draws a map made up of 32 pixel tiles, and allows the user to move the character with the arrow keys. Returns map positions and what the next action should be.  """
    pygame.init()
    tile_size = 32
    screen = pygame.display.set_mode((tile_size * 10, tile_size * 10))
    clock = pygame.time.Clock()

    try:
        player_image = pygame.image.load(Path.cwd().joinpath("sprites", "creatures", "player.png")).convert()
        player_image = pygame.transform.scale(player_image, (tile_size,tile_size))
    except:
        player_image = None
    try:
        monster_1_image = pygame.image.load(Path.cwd().joinpath("sprites", "creatures", f"{map_data["monster 1"].type}.png")).convert()
        monster_1_image = pygame.transform.scale(monster_1_image, (tile_size,tile_size))
    except:
        monster_1_image = None
    try:
        monster_2_image = pygame.image.load(Path.cwd().joinpath("sprites", "creatures", f"{map_data["monster 2"].type}.png")).convert()
        monster_2_image = pygame.transform.scale(monster_2_image, (tile_size,tile_size))
    except:
        monster_2_image = None

    moved = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit game"
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_UP and map_data["player_position"][1] > 0:
                map_data["player_position"][1] -= 1
                moved += 1
            elif event.key == pygame.K_DOWN and map_data["player_position"][1] < 9:
                map_data["player_position"][1] += 1
                moved += 1
            elif event.key == pygame.K_LEFT and map_data["player_position"][0] > 0:
                map_data["player_position"][0] -= 1
                moved += 1
            elif event.key == pygame.K_RIGHT and map_data["player_position"][0] < 9:
                map_data["player_position"][0] += 1
                moved += 1
            if moved % 2 == 0:
                map_data["monster 1"].move(map_data["town_position"])
                map_data["monster 2"].move(map_data["town_position"])


        screen.fill("antiquewhite2")
        pygame.draw.circle(screen, "green", ((map_data["town_position"][0] * tile_size) + (tile_size / 2), (map_data["town_position"][1] * tile_size) + (tile_size / 2)), 16)
        if monster_1_image:
            screen.blit(monster_1_image, (map_data["monster 1"].position[0] * tile_size, map_data["monster 1"].position[1] * tile_size))
        else:
            pygame.draw.circle(screen, map_data["monster 1"].color, ((map_data["monster 1"].position[0] * tile_size) + (tile_size / 2), (map_data["monster 1"].position[1] * tile_size) + (tile_size / 2)), 16)
        if monster_2_image:
            screen.blit(monster_2_image, (map_data["monster 2"].position[0] * tile_size, map_data["monster 2"].position[1] * tile_size))
        else:
            pygame.draw.circle(screen, map_data["monster 2"].color, ((map_data["monster 2"].position[0] * tile_size) + (tile_size / 2), (map_data["monster 2"].position[1] * tile_size) + (tile_size / 2)), 16)
        if player_image:
            screen.blit(player_image, (map_data["player_position"][0] * tile_size, map_data["player_position"][1] * tile_size))
        else:
            pygame.draw.rect(screen, "aquamarine3", pygame.Rect(map_data["player_position"][0] * tile_size, map_data["player_position"][1] * tile_size, 32, 32))
        pygame.display.flip()
        clock.tick(30)

        if moved == 0:
            continue
        elif map_data["player_position"] == map_data["town_position"]:
            next_action = "town menu"
            break
        elif map_data["player_position"] == map_data["monster 1"].position:
            next_action = "monster 1"
            break
        elif map_data["player_position"] == map_data["monster 2"].position:
            next_action = "monster 2"
            break

    pygame.quit()
    return next_action
