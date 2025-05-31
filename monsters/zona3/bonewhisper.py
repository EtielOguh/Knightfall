from random import randint
from monsters.mob import Enemy
from random import choice

class Bonewhisper(Enemy):
    def __init__(self):
        level = 7
        max_health = self._generate_max_health(level)
        health = max_health
        super().__init__(
            name="Bonewhisper",
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
        return f"{self.name} Appears! ATK: {self.attack} HP: {self.health}/{self.max_health}\nBonewhisper rattles its bones, but its attack is barely more than a nuisance."
