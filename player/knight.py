from .player_base import Player

class Knight(Player):
    def __init__(self):
        super().__init__(name="Knight", attack=25, defense=5, health=100)