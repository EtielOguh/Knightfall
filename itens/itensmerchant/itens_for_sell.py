from itens.archer import archer_weapons
from itens.knight import knight_shields, knight_swords
from itens.thief import thief_dagger
from itens.mage import mage_staffs
from itens.healm import universal_helm
from itens.armor import universal_armors
from itens.rarity import Rarity

rarity_level_limit = {
    1: Rarity.COMMON,
    5: Rarity.UNCOMMON,
    15: Rarity.RARE,
    30: Rarity.EPIC
}

def get_max_rarity_for_level(player_level):
    max_rarity = Rarity.COMMON
    for level, rarity in sorted(rarity_level_limit.items()):
        if player_level >= level:
            max_rarity = rarity
        else:
            break
    return max_rarity

def get_sellers_items(player):
    items_by_class = {
        1: knight_shields + knight_swords, 
        2: archer_weapons,
        3: thief_dagger,
        4: mage_staffs
    }

    class_specific_items = items_by_class.get(player.class_type, [])

    all_possible_items = class_specific_items + universal_armors + universal_helm

    max_rarity_allowed = get_max_rarity_for_level(player.level)

    buyable_items = [
        item for item in all_possible_items
        if item.rarity.value <= max_rarity_allowed.value and item.rarity != Rarity.DEVIL
    ]

    return buyable_items
    