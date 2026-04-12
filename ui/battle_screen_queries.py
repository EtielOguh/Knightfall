from battle.battle_inventory import BattleInventory
from world.zone import get_zone_name, get_zone_travel_options

class BattleScreenQueries:
    INVENTORY_CATEGORIES = ["weapon", "shield", "armor", "helmet", "jewel", "misc"]
    MENU_OPTIONS = ["Bag", "Equipped", "Close"]

    @staticmethod
    def get_bag_items(ui):
        return BattleInventory.get_bag_items(ui.player)

    @staticmethod
    def get_potion_items(ui):
        items = []

        if ui.player.healpotions > 0:
            items.append({
                "name": "Heal Potion",
                "quantity": ui.player.healpotions,
                "kind": "heal_potion"
            })

        if ui.player.manapotions > 0:
            items.append({
                "name": "Mana Potion",
                "quantity": ui.player.manapotions,
                "kind": "mana_potion"
            })

        return items

    @classmethod
    def get_inventory_categories(cls, ui):
        return cls.INVENTORY_CATEGORIES

    @classmethod
    def get_current_inventory_category(cls, ui):
        categories = cls.get_inventory_categories(ui)
        return categories[ui.state.inventory_category_index]

    @classmethod
    def get_inventory_items_by_category(cls, ui):
        current_category = cls.get_current_inventory_category(ui)

        return [
            item
            for item in ui.player.bag
            if getattr(item, "category", "misc") == current_category
        ]

    @staticmethod
    def get_equipped_items(ui):
        return [
            ("Right Hand", ui.player.right_hand[0] if ui.player.right_hand else None),
            ("Left Hand", ui.player.left_hand[0] if ui.player.left_hand else None),
            ("Body", ui.player.body[0] if ui.player.body else None),
            ("Head", ui.player.head[0] if ui.player.head else None),
        ]

    @classmethod
    def get_menu_options(cls, ui):
        return cls.MENU_OPTIONS
    
    @classmethod
    def get_menu_options(cls, ui):
        return ["Bag", "Equipped", "Zone Travel", "Close"]


    @staticmethod
    def get_zone_preview(ui):
        return get_next_zone_preview(ui.player)


    @staticmethod
    def get_current_zone_name(ui):
        return get_zone_name(ui.player.zone)
    
    @staticmethod
    def get_zone_travel_options(ui):
        return get_zone_travel_options(ui.player)