"""
game.py

This script imports and uses the gamefunctions module to provide basic 
game interactions, such as displaying a welcome message, shop menu, 
and generating a random monster.
"""

import gamefunction3

def main():
    """Main function to interact with the game."""
    player_name = input("Enter your name: ")
    gamefunction3.print_welcome(player_name)

    print("\nWelcome to the shop!")
    gamefunction3.print_shop_menu("Potion", 10, "Sword", 50)

    monster = gamefunction3.new_random_monster()
    print("\nA wild monster appears!")
    print(f"Name: {monster['name']}")
    print(f"Description: {monster['description']}")
    print(f"Health: {monster['health']}")
    print(f"Money: {monster['money']}")

if __name__ == "__main__":
    main()
