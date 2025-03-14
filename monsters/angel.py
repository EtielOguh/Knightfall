from mob import Enemy
from random import randint

class Angel(Enemy):
    def __init__(self, player):
        super().__init__(
            name="Angel",
            level=2,
            attack=self._generate_attack(),
            health=self._generate_health(player),
            max_health=self._generate_health(player)
        )

    def _generate_attack(self):
        return randint(0, 6)

    def _generate_health(self, player):
        return randint(player.max_health // 2, player.max_health)

    def battle_cry(self):
        return f"{self.name} Appears! HP: {self.health}/{self.max_health}\nFor my father, im gonna kill you!"
