from random import randint
from monsters.mob import Enemy
from itens.rarity import Rarity

class Deviloir(Enemy):
    def __init__(self):
        level = 4
        max_health = self._generate_max_health(level)
        health = max_health
        super().__init__(
            name="Deviloir",
            level=level,
            attack=self._generate_attack(level),
            health=health,
            max_health=max_health,
            ai_profile = "trickster",
            allowed_rarities=[Rarity.COMMON]
        )

    def _generate_attack(self, level):
        return randint(5 + level, 10 + level)

    def _generate_max_health(self, level):
        return 40 + (level * 20) + randint(0, 9)

    def battle_cry(self):
        return f"{self.name} Appears! Drowsywing flaps lazily, grazing you with a weak gust of air."