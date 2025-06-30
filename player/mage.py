from .player_base import Player

class Mage(Player):
    def __init__(self):
        super().__init__(name="Mage", attack=25, defense=2, health=100, type=4)