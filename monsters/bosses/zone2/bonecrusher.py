from monsters.mob import Enemy
from itens.rarity import Rarity
import random

class BoneCrusher(Enemy):
    def __init__(self):
        super().__init__(
            name="Bonecrusher",
            level=10,
            attack=30,
            health=400,
            max_health=400,
            allowed_rarities=[Rarity.UNCOMMON, Rarity.RARE],
            ai_profile="aggressive",
            is_boss=True
        )

    def decide_action(self, player):
        # ignora 30% da defesa do player
        if random.random() < 0.4:
            return {
                "type": "piercing_attack",
                "ignore_defense": 0.3,
                "label": "Bone Break"
            }

        return super().decide_action(player)