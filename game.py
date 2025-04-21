#Saige Vacca
#CSCI 150.50
#4.13.2025
#Assignment 12

"""
game.py

This script imports and uses the gamefunctions module to provide exciting
game interactions, such as displaying the initial welcome message and letting
adventurers choose their own path.
"""

import gamefunctions
import random
import wanderingMonster
play_game = True

shop_items = [
    {"name": "Sword", "type": "weapon", "uses": 10, "price":3, "description": "increases damage that you do by 10"},
    {"name": "Buckler", "type": "shield", "uses": 25, "price":3, "description": "reduces damage that you take a little bit."},
    {"name": "Shiny Ring", "type": "special item", "uses": 1, "price": 10, "description": "allows you to defeat one monster immediately, single use."}
]


start_menu = gamefunctions.main_menu()

if start_menu == "start_new_game":
    player_name = input("Enter your player name (Choose wisely!): ")

    player = {
        "HP": 30,
        "gold": 10,
        "name": player_name,
        "inventory": [],
        "equipped": {
            "weapon": {"name": "none"},
            "shield": {"name": "none"},
            "special item": {"name": "none"}
        }
    }

    map_data = {
        "player_position": None,
        "town_position": [random.randint(1,4), random.randint(1,8)],
        "monster 1": wanderingMonster.Monster(),
        "monster 2": wanderingMonster.Monster()
    }
    map_data["player_position"] = map_data["town_position"].copy()

elif start_menu == "load_save_file":
    player = {}
    map_data = {}
    gamefunctions.load_game(player, map_data)

gamefunctions.print_welcome(player["name"])



while play_game == True and player["HP"] > 0:
    gamefunctions.status_message(player)
    action_select = input("1) Leave town\n2) Sleep (Restore HP for 5 Gold)\n3) Browse Shop\n4) Change Equipment\n5) Save and Quit\n6) Quit Without Save\n")
    if action_select == "1":
        in_town = False
        while not in_town and player["HP"] > 0:
            next_action = gamefunctions.traverse_map(map_data)
            if "monster" in next_action:
                gamefunctions.monster_fight(player, map_data[next_action])
                if map_data["monster 1"].alive == False and map_data["monster 2"].alive == False:
                    map_data["monster 1"] = wanderingMonster.Monster()
                    map_data["monster 2"] = wanderingMonster.Monster()
            elif next_action == "town menu":
                print("You arrive back in to town after a long adventuring day.  Your eyes get heavy...")
                in_town = True
            elif next_action == "quit game":
                play_game = False
                break
    elif action_select == "2":
        gamefunctions.playersleep(player)
    elif action_select == "3":
        gamefunctions.shop_menu(player, shop_items)
    elif action_select == "4":
        gamefunctions.inventory_menu(player)
    elif action_select == "5":
        gamefunctions.save_game(player, map_data)
        break
    elif action_select == "6":
        break
    else:
        print("Try again Nerd!")

print("Game Over! Dun dun dunnn.")
