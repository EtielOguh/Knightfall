from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
from monsters.Infinityzone import monster_dynamic
from monsters.boss import boss_zone_1, boss_zone_2,boss_zone_3, boss_zone_4, boss_final
from random import choice, random, randint
import os
from copy import deepcopy
from itens.archer import archer_weapon
from itens.knight import knight_swords, knight_shields
from itens.thief import thief_dagger
from itens.mage import mage_staffs
from time import sleep
from itens.stone import Jewel_group
from itens.rarity import Rarity
    
def boss_fight(zone, player_level):
    bosses_by_zone = {
        1: boss_zone_1,
        2: boss_zone_2,
        3: boss_zone_3,
        4: boss_zone_4
    }

    while True:
        try:
            player_choice = int(input(
                "\nWhich boss do you want to fight against?\n"
                "1 - Boss from current zone\n"
                "2 - Final boss (Requires level 10+)\n"
                ">>> "
            ))
        except ValueError:
            print("Invalid input. Type 1 or 2.")
            continue

        if player_choice == 1:
            bosses = bosses_by_zone.get(zone)
            if bosses:
                return choice(bosses)()
            else:
                print("Invalid zone! Returning to the game.")
                return None 

        elif player_choice == 2:
            if player_level >= 10:
                return choice(boss_final)()
            else:
                print("You need to be at least level 10 for the final boss. Returning to the game.")
                return None

        else:
            print("Invalid option. Type 1 or 2.")
            continue

    
    
def spawn_monster(zone, player):
    if player.dynamic_zone == True:
       return choice(monster_dynamic)(player.level)
    elif zone == 1:
        return choice(monster_zona1)()
    elif zone == 2:
        return choice(monster_zona2)()
    elif zone == 3:
        return choice(monster_zona3)()
    elif zone == 4:
        return choice(monster_zona4)()
    else:
        raise ValueError("Invalid Zone")
    

def try_drop_stone(mob, player, drop_chance=0.2):
    if 1 <= mob.level <= 3:
        target_type = 1
    elif 4 <= mob.level <= 6:
        target_type = 2
    else:
        target_type = 3

    # Cria lista de CLASSES que combinam com o tipo do mob
    matching_stone_classes = [
        stone_class for stone_class in Jewel_group
        if stone_class().type == target_type
    ]

    if random() < drop_chance and matching_stone_classes:
        selected_class = choice(matching_stone_classes)
        new_stone = selected_class()
        new_stone.quantity += 1
        player.add_item_to_bag(new_stone)

        return new_stone

    return None


def get_droppable_items(player, mob):
    # Lista de itens por classe
    items_by_class = {
        1: knight_swords + knight_shields,  # Knight
        2: archer_weapon,                   # Archer
        3: thief_dagger, # Thief
        4: mage_staffs # Mage Itens
    }

    # Filtra os itens que têm raridade permitida no mob
    droppable_items = [
        item for item in items_by_class.get(player.class_type, [])
        if item.rarity in mob.allowed_rarities
    ]

    return droppable_items


def try_drop_item(player, mob):

    # Chances de drop por raridade (em %)
    rarities_with_chances = {
        Rarity.DEVIL: 0.5,      # 0.5%
        Rarity.EPIC: 1,         # 1%
        Rarity.RARE: 3,         # 3%
        Rarity.UNCOMMON: 5,     # 5%
        Rarity.COMMON: 10       # 10%
    }

    possible_items = get_droppable_items(player, mob)

    if not possible_items:
        print(f"{mob.name} Didn't drop anything useful for your class.")
        return None

    for rarity, chance in rarities_with_chances.items():
        roll = randint(1, 1000)  # Escala de 1000 pra suportar 0.5%
        if roll <= chance * 10:  # Ex: 0.5% vira 5 em 1000
            items_of_rarity = [item for item in possible_items if item.rarity == rarity]
            if items_of_rarity:
                dropped_item = choice(items_of_rarity)
                player.add_item_to_bag(dropped_item)
                print(f"{mob.name} Dropped: {dropped_item.name} | Attack: {dropped_item.attack} | Rarrity: ({rarity.name})")
                return dropped_item

    return None


def show_menu():
    print("\nA) Attack Enemy     B) Potion     Z) Change Zone   X) Back Zone   D) Dynamic Zone ON     P) Boss Fight")
    print("F) Run Enemy       I) Equip Iten     E) Show Bag        S) Save/Exit    H) Dynamic Zone OFF")
    action = input("Choose one > ").strip().lower()
    return action

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def merchant(self):
    print("\nBag Items:")
    for idx, item in enumerate(self.bag, 1):
        print(f"{idx}) {item}")
    print("0) Cancel and go back")

    while True:
        try:
            choice = int(input("\ntell me the item you want to sell: ")) - 1

            if choice == -1:
                print ("Returning to the game...")
                clear()
                return
            if choice < 0 or choice >= len(self.bag):
                print("Invalid number!")
                continue

            selected_item = self.bag[choice]

            money_gained = selected_item.price
            self.money += money_gained

            self.bag.pop(choice)

            print(f"You sold {selected_item.name} for R$ {selected_item.price} ")
            print(f"Current money R$ {self.money}")

            if len(self.bag) > 0:
                out = input("Do you want to sell more itens: [y|n]")
                if out == 'y':
                    continue
                if out == "n":
                    break
                else:
                    print("Invalid option, returning to the game...")
                    sleep(0.3)
                    break
            else:
                print ("You don't have itens do sell. Returning to the game...")
                sleep(0.3)
                break

        except ValueError:
            print("Please Choose a right option!")
