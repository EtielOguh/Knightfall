from random import randint
from monsters.mob import Enemy
from itens.rarity import Rarity

class DevilHell(Enemy):
    def __init__(self):
        level = 9
        attack = self._generate_attack(level)
        max_health = self._generate_max_health(level)
        health = max_health
        
        super().__init__(
            name="Devil Hell",
            level=level,
            attack=attack,
            health=health,
            max_health=max_health,
            allowed_rarities=[Rarity.DEVIL]
        )

    def _generate_attack(level):
        return randint(5 + level, 10 + level)

    def _generate_max_health(level):
        return 40 + (level * 20) + randint(0, 9)

    def battle_cry(self):
        return f"{self.name} Appears! ATK: {self.attack} HP: {self.health}/{self.max_health}\nThe Devil is more than just fire!"
