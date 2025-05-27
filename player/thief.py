from .player_base import Player

class Thief(Player):
    def __init__(self):
        super().__init__(name="Thief", attack=20, defense=3, health=90, type=3)