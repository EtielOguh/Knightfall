from monsters.mob import Enemy
from itens.rarity import Rarity
import random

class JokerReaper(Enemy):
    def __init__(self):
        super().__init__(
            name="Joker Reaper",
            level=5,
            attack=18,
            health=220,
            max_health=220,
            allowed_rarities=[Rarity.COMMON, Rarity.UNCOMMON],
            ai_profile="trickster",
            is_boss=True
        )

        self.status_chances = {
            "poison": 0.35
        }

    def battle_cry(self):
        return "The Reaper laughs... your end begins."

    def decide_action(self, player):
        # 30% chance de ataque duplo
        if random.random() < 0.3:
            return {
                "type": "double_attack",
                "multiplier": 0.8,
                "label": "Reaper Combo"
            }

        return super().decide_action(player)