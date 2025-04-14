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

play_game = True

shop_items = [
    {"name": "Sword", "type": "weapon", "uses": 10, "price":3, "description": "increases damage that you do by 10"},
    {"name": "Buckler", "type": "shield", "uses": 25, "price":3, "description": "reduces damage that you take a little bit."},
    {"name": "Shiny Ring", "type": "special item", "uses": 1, "price": 10, "description": "allows you to defeat one monster immediately, single use."}
]


start_menu = gamefunctions.main_menu()

if start_menu == "start_new_game":
    curr_HP = 30
    curr_gold = 10
    player_name = input("Enter your player name (Choose wisely!): ")
    curr_inventory = []
    curr_equipped = {
        "weapon": {"name": "none"},
        "shield": {"name": "none"},
        "special item": {"name": "none"}
    }
    map_positions = {
        "player_position": None,
        "town_position": [random.randint(1,4), random.randint(1,8)],
        "monster_position": [random.randint(6,9), random.randint(0,9)]
    }
    map_positions["player_position"] = map_positions["town_position"].copy()
elif start_menu == "load_save_file":
    player_name, curr_HP, curr_gold, curr_inventory, curr_equipped, map_positions = gamefunctions.load_game()

gamefunctions.print_welcome(player_name)



while play_game == True and curr_HP > 0:
    gamefunctions.status_message(curr_HP, curr_gold)
    action_select = input("1) Leave town\n2) Sleep (Restore HP for 5 Gold)\n3) Browse Shop\n4) Change Equipment\n5) Save and Quit\n6) Quit Without Save\n")
    if action_select == "1":
        in_town = False
        while not in_town:
            map_positions, next_action = gamefunctions.traverse_map(map_positions)
            if next_action == "fight monster":
                curr_HP, curr_gold, curr_equipped, map_positions["monster_position"] = gamefunctions.monster_fight(curr_HP, curr_gold, curr_equipped, map_positions["monster_position"])
            elif next_action == "town menu":
                print("You arrive back in to town after a long adventuring day.  Your eyes get heavy...")
                in_town = True
            elif next_action == "quit game":
                play_game = False
                break
    elif action_select == "2":
        curr_HP, curr_gold = gamefunctions.playersleep(curr_HP, curr_gold)
    elif action_select == "3":
        curr_gold, curr_inventory = gamefunctions.shop_menu(curr_gold, curr_inventory, shop_items)
    elif action_select == "4":
        curr_equipped, curr_inventory = gamefunctions.inventory_menu(curr_equipped, curr_inventory)
    elif action_select == "5":
        gamefunctions.save_game(player_name, curr_HP, curr_gold, curr_inventory, curr_equipped, map_positions)
        break
    elif action_select == "6":
        break
    else:
        print("Try again Nerd!")

print("Game Over! Dun dun dunnn.")
