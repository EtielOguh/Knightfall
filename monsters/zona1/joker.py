from random import randint
from monsters.mob import Enemy
from random import choice

class Joker(Enemy):
    def __init__(self):
        level = 1
        super().__init__(
            name="Joker",
            level=level,
            attack=self._generate_attack(level),
            health= 30,
            max_health=30
        )

    def _generate_attack(self, level):
        return randint(5 + level, 10 + level)

    def _generate_max_health(self, level):
        return 40 + (level * 20) + randint(0, 9)

    def battle_cry(self):
        return f"{self.name} Appears! HP: {self.health}/{self.max_health}\n Im just a JOKE HAHAHAHAHAHAHAH"