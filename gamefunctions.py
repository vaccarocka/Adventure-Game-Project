#Saige Vacca
#CSCI 150.50
#2.13.2025
#gamefunctions

import random

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1):
    if startingMoney >= itemPrice * quantityToPurchase:
        remainingMoney = startingMoney - itemPrice * quantityToPurchase
        return quantityToPurchase, remainingMoney
    else:
        max_affordable = int(startingMoney // itemPrice)
        remainingMoney = startingMoney - itemPrice * max_affordable
        return max_affordable, remainingMoney


def new_random_monster():
    monster_types = [
        {"name": "A vampire", "description": ["A pale, elegant vampire emerges from the shadows, its eyes glowing red.", "A bat flits across the moonlit sky. It might be a vampire in disguise.", "An ancient vampire, centuries old, rests in a coffin."], "health_range": (20, 35), "power_range": (7, 12), "money_range": (50, 150)},
        {"name": "A werewolf", "description": ["A creature with glowing yellow eyes and sharp claws lunges from the forest. It's a werewolf!", "A man with a strange mark on his neck seems nervous as the full moon approaches.", "A large wolf howls in the distance. Is it just a wolf, or something more?"], "health_range": (15, 25), "power_range": (5, 10), "money_range": (20, 80)},
        {"name": "A giant spider", "description": ["A massive spider descends from the trees, its eight eyes gleaming.", "A web stretches across your path. At its center sits a large, hairy spider.", "A small spider scuttles across the forest floor. But don't underestimate it!"], "health_range": (10, 25), "power_range": (3, 7), "money_range": (10, 30)}
    ]

    chosen_type = random.choice(monster_types)

    health = random.randint(*chosen_type["health_range"])
    power = random.randint(*chosen_type["power_range"])
    money = round(random.uniform(*chosen_type["money_range"]), 2) 
    description = random.choice(chosen_type["description"])

    monster = {
        "name": chosen_type["name"],
        "description": description,
        "health": health,
        "power": power,
        "money": money
    }
    return monster


# Demonstrate purchase_item()
print("Demonstrating purchase_item():")
num_purchased, leftover_money = purchase_item(1.23, 10, 3)
print(f"Purchased: {num_purchased}, Remaining money: {leftover_money}")

num_purchased, leftover_money = purchase_item(1.23, 2.01, 3)
print(f"Purchased: {num_purchased}, Remaining money: {leftover_money}")

num_purchased, leftover_money = purchase_item(3.41, 21.12)
print(f"Purchased: {num_purchased}, Remaining money: {leftover_money}")

num_purchased, leftover_money = purchase_item(31.41, 21.12)
print(f"Purchased: {num_purchased}, Remaining money: {leftover_money}")


# Demonstrate new_random_monster()
print("\nDemonstrating new_random_monster():")
for _ in range(3):  
    my_monster = new_random_monster()
    print(my_monster) 
    print(f"Name: {my_monster['name']}")
    print(f"Description: {my_monster['description']}")
    print(f"Health: {my_monster['health']}")
    print(f"Money: {my_monster['money']}")
    print("-" * 20)

def print_welcome(name: str, width: int = 20):
    """
    Prints a centered welcome message within the specified width.
    """
    message = f"Hello, {name}!!"
    print(f"{message:^{width}}")

def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float):
    """
    Prints a shop menu displaying 2 items with their prices, formatted with consistent spacing and a clean border.
    """
    border = "/" + "-" * 22 + "\\"
    item1 = f"| {item1Name:<12}${item1Price:>6.2f} |"
    item2 = f"| {item2Name:<12}${item2Price:>6.2f} |"
    print(border)
    print(item1)
    print(item2)
    print(border.replace("/", "\\").replace("\\", "/", 1))

#Demonstrate print_welcome()
print("\nDemonstrating print_welcome():")
print_welcome("Saige")
print_welcome("Sesame")
print_welcome("Christopher")

#Demonstrate print_shop_menu()
print("\nDemonstrating print_shop_menu():")
print_shop_menu("Tofu", 5, "Edamame", 3)
print_shop_menu("Broccoli", 2, "Basmati rice", 6)
print_shop_menu("Sriracha", 7, "Black beans", 1.50)
