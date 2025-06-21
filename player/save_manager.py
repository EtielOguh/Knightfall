import json
from itens.weapon import item_classes
from itens.rarity import Rarity


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
    print("💾 Save realizado com sucesso!")


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
        raise Exception("❌ Classe inválida no save.")

    # Carrega stats
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

    # Carrega itens
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

    print(f"✅ Save carregado com sucesso! Bem-vindo de volta, {player.name}.")

    return player
