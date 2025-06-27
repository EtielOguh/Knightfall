from random import randint
from monsters.mob import Enemy
from itens.rarity import Rarity

class GoblinKing(Enemy):
    def __init__(self):
        level = 9
        attack = self._generate_attack(level)
        max_health = self._generate_max_health(level)
        health = max_health
        
        super().__init__(
            name="Goblin King",
            level=level,
            attack=attack,
            max_health=max_health,
            health=health,
            allowed_rarities=[Rarity.UNCOMMON]
        )

    @staticmethod
    def _generate_attack(level):
        return randint(5 + level, 10 + level)
    
    @staticmethod
    def _generate_max_health(level):
        return 40 + (level * 20) + randint(0, 9)


    def battle_cry(self):
        return f"{self.name} Appears! ATK: {self.attack} HP: {self.health}/{self.max_health}\nThe Devil is more than just fire!"
