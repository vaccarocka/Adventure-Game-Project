#Saige Vacca
#CSCI 150.50
#3.30.2025
#Assignment 10

"""This module contains functions for my simple text-based game, including a
vegetarian shop system and random monster generation. Functions include
printing a welcome messages, displaying a veggie-friendly shop menu, handling
item purchases, and creating random monsters!
    print_welcome("Player")
    print_shop_menu("Sword", 10, "Shield", 15)
    quantity, remaining = purchase_item(10, 50, 2)
    monster = new_random_monster()"""

import random

def print_welcome(name: str, width: int = 20) -> None:
    """Print a centered welcome message within the specified width.
    Parameters: name (str): The name of the player. width (int, optional):
    The width of the message formatting. Defaults to 20. Returns: None"""
    message = f"Hello, {name}!!"
    print(f"{message:^{width}}")

def status_message(Player_start_HP, Player_start_Gold):
    """Welcome the player with setting and current player status."""
    print("You wake up in a quiet and secluded forest town.")
    print(f"Current HP: {Player_start_HP}, Current Gold: {Player_start_Gold}")
    print("What would you like to do?")

def combat_function(monster_start_HP, Player_start_HP, player_equipment):
    """Display and run turn based combat between player and monster. Returns
    player and monster HP values post-battle."""
    monst_damage_pl = random.randint(2,7)
    if player_equipment["shield"]["name"] == "buckler":
        monst_damage_pl -= random.randint(3,8)
        if monst_damage_pl <= 0:
            monst_damage_pl = 0
            print("The monster tried to claw at you, but your shield negated all damage!")
        else:
            print(f"The monster attacked, but the shield reduced damage to just {monst_damage_pl}. Phew!")
        player_equipment["shield"]["uses"] -= 1
        if player_equipment["shield"]["uses"] < 1:
            player_equipment["shield"] = {"name": "none"}
            print("Your shield snaps in half!!!")
    else:
        print(f"You take a blow! Damage dealt by monster: {monst_damage_pl}!")
    Player_start_HP = Player_start_HP - monst_damage_pl
    player_damage_monst = random.randint(1,15)
    if player_equipment["weapon"]["name"] == "sword":
        player_damage_monst += 10
        print(f"You draw your weapon and swing! You land a blow. Damage dealt by player: {player_damage_monst}!")
        player_equipment["weapon"]["uses"] -= 1
        if player_equipment["weapon"]["uses"] < 1:
            player_equipment["weapon"] = {"name": "none"}
            print("Your sword snaps in half!!!")
    else:
        print(f"You karate chop the monster! Damage dealt by player: {player_damage_monst}!")

    monster_start_HP = monster_start_HP - player_damage_monst
    return (monster_start_HP, Player_start_HP, player_equipment)

def monster_fight(Player_start_HP, Player_start_Gold, player_equipment):
    """Introduces monster and runs combat loop, prompting player to fight to the
    death or flee. Returns player HP and gold."""
    print("You hear footsteps behind you. You turn around and see ... a monster! It lunges towards you.")
    monster_start_HP = 40
    while Player_start_HP > 0 and monster_start_HP > 0:
        if player_equipment["weapon"]["name"] == "sword":
            print(f"You currently have a sword equipped.  It increases your damage by 10, and has {player_equipment["weapon"]["uses"]} uses left.")
        if player_equipment["shield"]["name"] == "buckler":
            print(f"You currently have a buckler equipped.  It reduces your damage by a number from 3 to 8, and has {player_equipment["shield"]["uses"]} uses left.")
        fight_options = "1) Fight!\n2) Flee!\n"
        if player_equipment["special item"]["name"] == "shiny ring":
            print(f"You currently have a shiny ring equipped.  It has {player_equipment["special item"]["uses"]} uses left.")
            fight_options += "3) Befriend monster using the Shiny Ring"
        print(f"Player Current HP: {Player_start_HP}, Monster Current HP: {monster_start_HP}")
        Fight_selection = input(fight_options)
        if Fight_selection == "1":
            monster_start_HP, Player_start_HP, player_equipment = combat_function(monster_start_HP, Player_start_HP, player_equipment)
        elif Fight_selection == "2":
            break
        elif Fight_selection == "3" and player_equipment["special item"]["name"] == "shiny ring":
            print("You reveal the shiny ring, and the monster says, \"I've been looking for this! Thanks you so very much!\" and they run back into the forest (leaving behind a pile of gold coins).")
            player_equipment["special item"] = {"name": "none"}
            monster_start_HP = 0
        else:
            print("Try again Nerd!")
    if monster_start_HP < 1 and Player_start_HP > 0:
        winner_gold = random.randint(1,10)
        Player_start_Gold = Player_start_Gold + winner_gold
        print(f"You defeat the monster. You find {winner_gold} Gold as your eyes get heavy...")
    return Player_start_HP, Player_start_Gold, player_equipment

def playersleep(player_start_HP, player_gold):
    """Introduces sleep option to player. Subtracts gold for gained HP. Returns
    player HP and gold."""
    print("You follow a beaten path to a clearing that reveals an Inn. It seems tattered and rickety, but the aroma of fresh bread and the promise of soft pillows draw you in.")
    print("You encounter the Innkeeper. They take 5 Gold from you and point you towards your room for the night.")
    player_gold = player_gold - 5
    player_start_HP = player_start_HP + 10
    return (player_start_HP, player_gold)

def display_items(item_list, detail_list=[]):
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
    item_names = []
    for item in item_list:
        item_names.append(item["name"].lower())
    return item_names

def get_item_by_name(item_list, name):
    for item in item_list:
        if item["name"] == name:
            return item

def get_items_by_type(item_list, type):
    new_item_list = []
    for item in item_list:
        if item["type"] == type:
            new_item_list.append(item)
    return new_item_list

def remove_item_by_name(item_list, name):
    for i in range(len(item_list)):
        if item_list[i]["name"] == name:
            item_list.pop(i)
            return item_list

def purchase_item(player_gold, player_inventory, item):
    if player_gold >= item["price"]:
        player_gold -= item["price"]
        player_inventory.append(item)
    else:
        print(f"Sorry, {item["name"]} costs {item["price"]}, but you only have {player_gold} gold.")
    return player_gold, player_inventory

def shop_menu(player_gold, player_inventory, shop_inventory):
    print("\nYou enter the shop and are greeted by the shopkeep")
    while True:
        print(f"Current gold: {player_gold}\nYour current inventory: {display_items(player_inventory)}")
        print(f"Shop inventory: {display_items(shop_inventory, ["type", "price"])}")
        shop_select = input("Type the name of the item you would like to buy, or 'Q' to quit\n")
        if shop_select.lower() == "q":
            return player_gold, player_inventory
        elif shop_select.lower() in get_item_names(shop_inventory):
            for item in shop_inventory:
                if item["name"] == shop_select:
                    player_gold, player_inventory = purchase_item(player_gold, player_inventory, item)
                    break
        else:
            print(f"Sorry, I don't know what a {shop_select} is.")

def equip_item(player_equipment, player_inventory, type):
    if player_equipment[type]["name"] != "none":
        player_inventory.append(player_equipment[type])
    print(f"Which item to equip as {type}? {display_items(get_items_by_type(player_inventory, type))}")
    while True:
        equip_select = input("Type the name of the item you would like to equip.\n")
        if equip_select in get_item_names(get_items_by_type(player_inventory, type)):
            for item in player_inventory:
                if item["name"] == equip_select:
                    player_equipment[type] = item
                    player_inventory = remove_item_by_name(player_inventory, item["name"])
                    return player_equipment, player_inventory
        else:
            print("Sorry, you didn't enter the name of an item.")

def inventory_menu(player_equipment, player_inventory):
    while True:
        print(f"\nYour current inventory: {display_items(player_inventory, ["type", "uses"])}")
        print(f"Currently equipped items:\nWeapon: {player_equipment["weapon"]["name"]}\nShield: {player_equipment["shield"]["name"]}\nSpecial Item: {player_equipment["special item"]["name"]}")
        inventory_select = input("Type 'Weapon', 'Shield', or 'Special Item' to change equipment.  Type 'Q' to quit.").lower()
        if inventory_select == "q":
            return player_equipment, player_inventory
        elif inventory_select == "weapon" or inventory_select == "shield" or inventory_select == "special item":
            player_equipment, player_inventory = equip_item(player_equipment, player_inventory, inventory_select)
        else:
            print(f"Sorry, I don't recognize equipment type: {inventory_select}")

    return equipment, inventory
