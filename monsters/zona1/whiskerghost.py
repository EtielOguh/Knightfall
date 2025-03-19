from random import randint
from mob import Enemy

class Whiskerghost(Enemy):
    def __init__(self):
        level = 3
        max_health = self._generate_max_health(level)
        health = max_health
        super().__init__(
            name="Whiskerghost",
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
        return f"{self.name} Appears! HP: {self.health}/{self.max_health}\nWhiskerghost flickers in and out, giving you a spooky chill but no real harm."
