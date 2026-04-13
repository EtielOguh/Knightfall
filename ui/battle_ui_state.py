class BattleUIState:
    def __init__(self):
        self.show_bag = False
        self.bag_index = 0
        self.show_potions = False
        self.potion_index = 0
        self.show_zone_menu = False
        self.zone_menu_index = 0

        self.show_menu = False
        self.show_inventory = False
        self.show_equipped = False
        self.show_skills = False
        self.skill_index = 0
        self.inventory_category_index = 0
        self.inventory_item_index = 0
        self.menu_index = 0
        self.equipped_index = 0

        self.log_messages = []

        self.zone_transition_active = False
        self.zone_transition_phase = None
        self.zone_transition_alpha = 0
        self.pending_zone_id = None
        self.zone_title_timer = 0
        self.zone_title_text = ""

    def add_log(self, text: str, log_type="combat") -> None:
            entry = {
                "text": str(text),
                "type": log_type
            }

            # Se for evento importante, limpa só o lixo antes
            if log_type == "important":
                self.log_messages = [
                    e for e in self.log_messages
                    if e["type"] != "combat"
                ]

            self.log_messages.append(entry)

            # limite geral
            if len(self.log_messages) > 8:
                self.log_messages.pop(0)