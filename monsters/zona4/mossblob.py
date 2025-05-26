from random import randint
from monsters.mob import Enemy
from random import choice

class Mossblob(Enemy):
    def __init__(self):
        level = 9
        max_health = self._generate_max_health(level)
        health = max_health
        super().__init__(
            name="Mossblob",
            level=level,
            attack=self._generate_attack(level),
            health=health,
            max_health=max_health
        )

    def _generate_attack(self, level):
        return randint(5 + level, 10 + level)

    def _generate_max_health(self, level):
        return 40 + (level * 20) + randint(0, 9)

    def battle_cry(self):
        return f"{self.name} Appears! HP: {self.health}/{self.max_health}\nMossblob oozes slowly toward you, its slimy body slowing you down slightly."