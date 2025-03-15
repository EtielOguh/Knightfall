from random import randint
from mob import Enemy

class Dragon(Enemy):
    def __init__(self):
        super().__init__(
            name="Dragon",
            level=2,
            attack=self._generate_attack(),
            health=self._generate_health(),
            max_health=self._generate_health()
        )

    def _generate_attack(self):
        return randint(5 + self.level, 10 + self.level)  # Cresce com o nível

    def _generate_health(self):
        return 80 + (self.level * 20) + randint(0, 10)  # Vida baseada no nível

    def battle_cry(self):
        return f"{self.name} Appears! HP: {self.health}/{self.max_health}\nFor my father, im gonna kill you!"
