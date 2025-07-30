import os
import json
from itens.rarity import Rarity

from player.knight import Knight
from player.archer import Archer
from player.thief import Thief
from player.mage import Mage
    
from itens.knight import knight_swords, knight_shields
from itens.archer import archer_weapon
from itens.thief import thief_dagger
from itens.mage import mage_staffs

#import dos itens das classes
from itens.knight.knight_weapon import *
from itens.archer.archer_weapon import *
from itens.thief.thief_weapon import *
from itens.mage.mage_weapon import *

from itens.stone import Jewel_group  # Importa as classes das joias

# 🔗 Item classes automático (armas)
item_classes = {
    **{item.name: item.__class__ for item in knight_swords},
    **{item.name: item.__class__ for item in knight_shields},
    **{item.name: item.__class__ for item in archer_weapon},
    **{item.name: item.__class__ for item in thief_dagger},
    **{item.name: item.__class__ for item in mage_staffs}
}

# Adiciona as classes das joias ao dicionário de classes
item_classes.update({cls().name: cls for cls in Jewel_group})


def chose_class():

    print("1 – Knight | 2 – Archer | 3 – Thief | 4 - Mage")
    choice = input("> Choose (1, 2, 3 or 4): ").strip()

    if choice == "1":
        player = Knight()
    elif choice == "2":
        player = Archer()
    elif choice == "3":
        player = Thief()
    elif choice == "4":
        player = Mage()
    else:
        print("Invalid choice, now your class is a Knight (default)")
        player = Knight()

    return player


def serialize_item(item):
    data = vars(item).copy()
    if hasattr(item, "rarity"):
        data["rarity"] = item.rarity.name
    if hasattr(item, "quantity"):
        data["quantity"] = item.quantity
    if hasattr(item, "type"):
        data["type"] = item.type
    return data


def serialize_items(items):
    return [serialize_item(item) for item in items]


def save_player(player, filename="save_data.json"):
    data = {
        "name": player.name,
        "class_type": player.class_type,
        "level": player.level,
        "attack": player.attack,
        "defense": player.defense,
        "health": player.health,
        "max_health": player.max_health,
        "zone": player.zone,
        "xp": player.xp,
        "xp_max": player.xp_max,
        "money": player.money,
        "mana_potions": player.manapotions,
        "heal_potions": player.healpotions,
        "dynamic_zone": player.dynamic_zone,
        "bag": serialize_items(player.bag),
        "right_hand": serialize_items(player.right_hand),
        "left_hand": serialize_items(player.left_hand),
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_player(filename="save_data.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    from player.knight import Knight
    from player.archer import Archer
    from player.thief import Thief

    if data["class_type"] == 1:
        player = Knight()
    elif data["class_type"] == 2:
        player = Archer()
    elif data["class_type"] == 3:
        player = Thief()
    elif data["class_type"] == 4:
        player = Mage()
    else:
        raise Exception("Invalid Class.")

    player.name = data["name"]
    player.level = data["level"]
    player.attack = data["attack"]
    player.defense = data["defense"]
    player.health = data["health"]
    player.max_health = data["max_health"]
    player.zone = data["zone"]
    player.xp = data["xp"]
    player.xp_max = data["xp_max"]
    player.money = data["money"]
    player.manapotions = data["mana_potions"]
    player.healpotions = data["heal_potions"]
    player.dynamic_zone = data.get("dynamic_zone", False)

    def load_items(item_list):
        items = []
        for i in item_list:
            cls = item_classes.get(i["name"])
            if cls:
                item = cls(price=i.get("price", 0))
                if "rarity" in i:
                    item.rarity = Rarity[i["rarity"]]
                if "quantity" in i:
                    item.quantity = i["quantity"]
                if "type" in i:
                    item.type = i["type"]
                items.append(item)
        return items

    player.bag = load_items(data.get("bag", []))
    player.right_hand = load_items(data.get("right_hand", []))
    player.left_hand = load_items(data.get("left_hand", []))
    return player


def load_or_create_player():
    if os.path.exists("save_data.json"):
        try:
            player = load_player()
            print(f"Player {player.name} Loaded successfully!")
            return player
        except Exception as e:
            print(f"\n Error!: {e}")
            print("Creating a new player...")
    else:
        print("No save file found. Starting a new player...")

    return chose_class()
