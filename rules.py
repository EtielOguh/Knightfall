from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
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
from monsters.bosses.zone1 import boss_zone1
from monsters.bosses.zone2 import boss_zone2
from monsters.bosses.zone3 import boss_zone3
from monsters.bosses.zone4 import boss_zone4

def spawn_boss(zone,player):
    if zone ==1:
        return choice(boss_zone1)()
    if zone == 2:
        return choice(boss_zone2)()
    if zone ==3:
        return choice(boss_zone3)()
    elif zone ==4:
        return choice(boss_zone4)()
    else:
        return ValueError("Invalid Zone")
    
def spawn_monster(zone, player):
    if zone == 1:
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

def try_drop_item(player, mob):
    DROP_CHANCE = 0.4

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
    chosen_rarity = None

    for rarity, weight in rarities:
        cumulative += weight
        if roll <= cumulative:
            chosen_rarity = rarity
            break

    possible_items = get_droppable_items(player, mob)

    items_of_rarity = [
        item_class for item_class in possible_items
        if item_class().rarity == chosen_rarity
    ]

    if not items_of_rarity:
        return None

    selected_class = choice(items_of_rarity)
    dropped_item = selected_class()

    player.add_item_to_bag(dropped_item)
    return dropped_item

universal_items = universal_helm + universal_armors # Capacete de Couro, Capacete de Ferro, etc.

def get_droppable_items(player, mob):
    items_by_class = {
        1: knight_swords + knight_shields,
        2: archer_weapons,
        3: thief_dagger,
        4: mage_staffs
    }

    class_specific_items = items_by_class.get(player.class_type, [])
    all_possible_drops = class_specific_items + universal_items

    droppable_items = [
        item_class for item_class in all_possible_drops
        if item_class().rarity in mob.allowed_rarities
    ]

    return droppable_items


def try_drop_item(player, mob):
    DROP_CHANCE = 0.4

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
    chosen_rarity = None

    for rarity, weight in rarities:
        cumulative += weight
        if roll <= cumulative:
            chosen_rarity = rarity
            break

    possible_items = get_droppable_items(player, mob)
    items_of_rarity = [item_class for item_class in possible_items if item_class().rarity == chosen_rarity]

    if not items_of_rarity:
        return None

    selected_class = choice(items_of_rarity)
    dropped_item = selected_class()

    player.add_item_to_bag(dropped_item)
    return dropped_item

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
