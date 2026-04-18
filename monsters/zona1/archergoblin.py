from random import randint
from monsters.mob import Enemy
from itens.rarity import Rarity

class Archergoblin(Enemy):
    def __init__(self):
        level = 2
        max_health = self._generate_max_health(level)
        health = max_health
        super().__init__(
            name="Archer Goblin",
            level=level,
            attack=self._generate_attack(level),
            health=health,
            max_health=max_health,
            ai_profile = "trickster",
            allowed_rarities=[Rarity.COMMON]
        )

        self.status_chances = {
            "poison": 0.25
        }

    def _generate_attack(self, level):
        return randint(5 + level, 10 + level)

    def _generate_max_health(self, level):
        return 40 + (level * 20) + randint(0, 9)

    def battle_cry(self):
        return f"{self.name} Appears! Whiskerghost flickers in and out, giving you a spooky chill but no real harm."
