#Saige Vacca
#CSCI 150.50
#3.9.2025
#gamefunctions.assignment8

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

def combat_function(monster_start_HP, Player_start_HP):
    """Display and run turn based combat between player and monster. Returns
    player and monster HP values post-battle."""
    monst_damage_pl = random.randint(2,7)
    print(f"You take a blow! Damage dealt by monster: {monst_damage_pl}!")
    Player_start_HP = Player_start_HP - monst_damage_pl
    player_damage_monst = random.randint(1,15)
    print(f"You draw your weapon and swing! You land a blow. Damage dealt by player: {player_damage_monst}!")
    monster_start_HP = monster_start_HP - player_damage_monst
    return (monster_start_HP, Player_start_HP)

def monster_fight(Player_start_HP, Player_start_Gold):
    """Introduces monster and runs combat loop, prompting player to fight to the
    death or flee. Returns player HP and gold."""
    print("You hear footsteps behind you. You turn around and see ... a monster! It lunges towards you.")
    monster_start_HP = 40
    while Player_start_HP > 0 and monster_start_HP > 0:
        print(f"Player Current HP: {Player_start_HP}, Monster Current HP: {monster_start_HP}")
        Fight_selection = input("1) Fight!\n2) Flee!\n")
        if Fight_selection == "1":
            monster_start_HP, Player_start_HP = combat_function(monster_start_HP, Player_start_HP)
        elif Fight_selection == "2":
            break
        else:
            print("Try again Nerd!")
    if monster_start_HP < 1 and Player_start_HP > 0:
        winner_gold = random.randint(1,10)
        Player_start_Gold = Player_start_Gold + winner_gold
        print(f"You defeat the monster. You find {winner_gold} Gold as your eyes get heavy...")
    return Player_start_HP, Player_start_Gold

def playersleep(player_start_HP, player_gold):
    """Introduces sleep option to player. Subtracts gold for gained HP. Returns
    player HP and gold."""
    print("You follow a beaten path to a clearing that reveals an Inn. It seems tattered and rickety, but the aroma of fresh bread and the promise of soft pillows draw you in.")
    print("You encounter the Innkeeper. They take 5 Gold from you and point you towards your room for the night.")
    player_gold = player_gold - 5
    player_start_HP = player_start_HP + 10
    return (player_start_HP, player_gold)
