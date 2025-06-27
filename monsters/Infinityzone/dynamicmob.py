from monsters.mob import Enemy
from itens.rarity import Rarity
from random import randint, choice

class DynamicMob(Enemy):
    def __init__(self, player_level):
        name = choice(["Shade Crawler", "Rustfang", "Gloom Imp", "Ashling", "Feral Wisp", "Fly Bird"])
        level = max(1, player_level - 1)
        attack = max(1, player_level * randint(2, 4) // 3)
        health = player_level * randint(10, 15)
        max_health = health

        super().__init__(
            name=name,
            level=level,
            attack=attack,
            health=health,
            max_health=max_health,
            allowed_rarities=[Rarity.RARE, Rarity.EPIC]
        )

    def battle_cry(self):
        return f"{self.name} rises from the shadows! ATK: {self.attack} HP: {self.health}/{self.max_health}\nYou feel a strange familiarity..."
