from random import randint
from monsters.mob import Enemy
from itens.rarity import Rarity

class Warriorgoblin(Enemy):
    def __init__(self):
        level = 1
        max_health = self._generate_max_health()
        health = max_health
        super().__init__(
            name="Warrior Goblin",
            level=level,
            attack=self._generate_attack(),
            health=health,
            max_health=max_health,
            allowed_rarities=[Rarity.COMMON]
        )

    def _generate_attack(self):
        return randint(15, 25)

    def _generate_max_health(self):
        return randint (60, 90)

    def battle_cry(self):
        return f"{self.name} Appears! Spiketooth nicks you with its tiny, sharp teeth. It barely hurts."
    

