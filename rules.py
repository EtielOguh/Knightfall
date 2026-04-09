from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
from monsters.Infinityzone import monster_dynamic
from monsters.boss import boss_zone_1, boss_zone_2,boss_zone_3, boss_zone_4, boss_final
from random import choice, random, randint
import os
from itens.archer import archer_weapons
from itens.knight import knight_swords, knight_shields
from itens.thief import thief_dagger
from itens.mage import mage_staffs
from itens.healm import universal_helm
from itens.armor import universal_armors
from time import sleep
from itens.stone.stone_registry import STONE_BY_TYPE
from itens.rarity import Rarity
from random import random, choice, choices
    
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
    

def get_stone_type(level):
    if level <= 3:
        return 1
    if level <= 6:
        return choices([2, 1], weights=[75, 25])[0]
    return choices([3, 2, 1], weights=[70, 20, 10])[0]


def get_stone_drop_chance(level, is_boss=False):
    if is_boss:
        return 1.0
    if level <= 3:
        return 0.15
    if level <= 6:
        return 0.20
    return 0.25


def try_drop_stone(mob, player, is_boss=False):
    drop_chance = get_stone_drop_chance(mob.level, is_boss)

    if random() > drop_chance:
        return None

    target_type = get_stone_type(mob.level)

    matching_stone_classes = STONE_BY_TYPE.get(target_type, [])

    if not matching_stone_classes:
        return None

    selected_class = choice(matching_stone_classes)
    new_stone = selected_class()

    player.add_item_to_bag(new_stone)
    return new_stone

universal_items = universal_helm + universal_armors # Capacete de Couro, Capacete de Ferro, etc.

def get_droppable_items(player, mob):
    items_by_class = {
        1: knight_swords + knight_shields,
        2: archer_weapons,
        3: thief_dagger,
        4: mage_staffs
    }

    class_items = items_by_class.get(player.class_type, [])
    all_items = class_items + universal_items

    return [
        item_class for item_class in all_items
        if item_class().rarity in mob.allowed_rarities
    ]


def try_drop_item(player, mob):
    DROP_CHANCE = 0.4  # Aqui troca a % de chance de dropar algo, está em 40% por padrão

    if random() > DROP_CHANCE:
        return None

    rarities = [
        (Rarity.COMMON, 60),
        (Rarity.UNCOMMON, 25),
        (Rarity.RARE, 10),
        (Rarity.EPIC, 4),
        (Rarity.DEVIL, 1),
    ]

    roll = randint(1, 100)
    cumulative = 0

    for rarity, weight in rarities:
        cumulative += weight
        if roll <= cumulative:
            chosen_rarity = rarity
            break

    possible_items = get_droppable_items(player, mob)
    items_of_rarity = [i for i in possible_items if i().rarity == chosen_rarity]

    if not items_of_rarity:
        return None

    dropped_item = choice(items_of_rarity)
    player.add_item_to_bag(dropped_item)

    return dropped_item

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
