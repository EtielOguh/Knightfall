from mob import Enemy
from random import randint

class Goblin(Enemy):
    def __init__(self, player):
        super().__init__(
            name="Goblin",
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
        return f"{self.name} is gonna kill you! {self.health}/{self.max_health}"
