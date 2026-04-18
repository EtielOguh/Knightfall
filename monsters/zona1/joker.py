from random import randint
from monsters.mob import Enemy
from random import choice
from itens.rarity import Rarity

class Joker(Enemy):
    def __init__(self):
        level = 1
        super().__init__(
            name="Joker",
            level=level,
            attack=5,
            health= 50,
            max_health=50,
            ai_profile = "trickster",
            allowed_rarities=[None]
        )

        self.status_chances = {
            "poison": 0.25
        }


    def battle_cry(self):
        return f"{self.name} Appears! Im just a JOKE HAHAHAHAHAHAHAH"