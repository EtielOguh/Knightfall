from random import randint
from monsters.mob import Enemy
from random import choice
from itens.swords import swords
from itens.shields import shields

class Twirlbeast(Enemy):
    def __init__(self):
        level = 8
        max_health = self._generate_max_health(level)
        health = max_health
        super().__init__(
            name="Twirlbeast",
            level=level,
            attack=self._generate_attack(level),
            health=health,
            max_health=max_health
        )
        self.drop_items = [swords[1], shields[1]]

    def _generate_attack(self, level):
        return randint(5 + level, 10 + level)

    def _generate_max_health(self, level):
        return 40 + (level * 20) + randint(0, 9)

    def battle_cry(self):
        return f"{self.name} Appears! HP: {self.health}/{self.max_health}\nTwirlbeast spins around, bumping into you accidentally, causing no real harm."

    def drop_loot(self):
        drop_item = choice(self.drop_items)

        if randint(1, 100) <= 50:
            print(f"{self.name} dropped {drop_item.name}!")
            return drop_item
        else:
            print(f"{self.name} didn't drop anything this time.")
            return None