#Saige Vacca
#CSCI 150.50
#3.25.2025
#Assignment 9

"""
game.py

This script imports and uses the gamefunctions module to provide exciting
game interactions, such as displaying the initial welcome message and letting
adventurers choose their own path.
"""

import gamefunctions3
import random

player_name = input("Enter your player name (Choose wisely!): ")
gamefunctions3.print_welcome(player_name)
curr_HP = 30
curr_gold = 10
play_game = True

while play_game == True:
    gamefunctions3.status_message(curr_HP, curr_gold)
    action_select = input("1) Leave town (Fight Monster)\n2) Sleep (Restore HP for 5 Gold)\n3) Quit\n")
    if action_select == "1":
        curr_HP, curr_gold = gamefunctions3.monster_fight(curr_HP, curr_gold)
        if curr_HP < 1:
            break
    elif action_select == "2":
        curr_HP, curr_gold = gamefunctions3.playersleep(curr_HP, curr_gold)
    elif action_select == "3":
        break
    else:
        print("Try again Nerd!")

print("Game Over! Dun dun dunnn.")
