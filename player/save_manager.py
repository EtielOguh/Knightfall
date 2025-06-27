import os
import json
from itens.rarity import Rarity

from itens.knight import knight_swords, knight_shields
from itens.archer import archer_weapon
from itens.thief import thief_dagger

from itens.knight.knight_weapon import *
from itens.archer.archer_weapon import *
from itens.thief.thief_weapon import *

# 🔗 Item classes automático
item_classes = {
    **{item.name: item.__class__ for item in knight_swords},
    **{item.name: item.__class__ for item in knight_shields},
    **{item.name: item.__class__ for item in archer_weapon},
    **{item.name: item.__class__ for item in thief_dagger}
}


def chose_class():
    from player.knight import Knight
    from player.archer import Archer
    from player.thief import Thief

    print("1 – Knight | 2 – Archer | 3 – Thief")
    choice = input("> Choose (1, 2, or 3): ").strip()

    if choice == "1":
        player = Knight()
    elif choice == "2":
        player = Archer()
    elif choice == "3":
        player = Thief()
    else:
        print("Invalid choice, now your class is a Knight (default)")
        player = Knight()

    return player


def serialize_item(item):
    data = vars(item).copy()
    if hasattr(item, "rarity"):
        data["rarity"] = item.rarity.name
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
        "potion": player.potion,
        "dynamic_zone": player.dynamic_zone,
        "bag": serialize_items(player.bag),
        "right_hand": serialize_items(player.right_hand),
        "left_hand": serialize_items(player.left_hand),
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Successfully Save!")


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
    player.potion = data["potion"]
    player.dynamic_zone = data.get("dynamic_zone", False)

    def load_items(item_list):
        items = []
        for i in item_list:
            item = item_classes[i["name"]](price=i.get("price"))
            if "rarity" in i:
                item.rarity = Rarity[i["rarity"]]
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
