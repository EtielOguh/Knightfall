from monsters.mob import Enemy
from itens.rarity import Rarity
import random

class DinosBraker(Enemy):
    def __init__(self):
        super().__init__(
            name="Demon Overlord",
            level=20,
            attack=60,
            health=900,
            max_health=900,
            allowed_rarities=[Rarity.RARE, Rarity.EPIC],
            ai_profile="aggressive",
            is_boss=True
        )

        self.rage_activated = False

    def decide_action(self, player):
        hp_ratio = self.health / self.max_health

        if hp_ratio < 0.3 and not self.rage_activated:
            self.attack += 20
            self.rage_activated = True
            return {"type": "buff", "label": "Dino Ranger"}

        return super().decide_action(player)