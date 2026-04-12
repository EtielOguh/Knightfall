class BattleUIState:
    def __init__(self):
        self.show_bag = False
        self.bag_index = 0
        self.show_potions = False
        self.potion_index = 0
        self.show_zone_menu = False
        self.zone_menu_index = 0
        self.show_menu = False
        self.menu_index = 0

        self.show_inventory = False
        self.inventory_category_index = 0
        self.inventory_item_index = 0

        self.show_equipped = False
        self.show_skills = False
        self.skill_index = 0
        self.equipped_index = 0

        self.logs = ["Battle started."]

    def add_log(self, text: str) -> None:
        self.logs.append(str(text))
        if len(self.logs) > 6:
            self.logs.pop(0)