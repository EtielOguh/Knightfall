from .player_base import Player

class Archer(Player):
    def __init__(self):
        super().__init__(name="Archer", attack=30, defense=3, health=100, type=2)