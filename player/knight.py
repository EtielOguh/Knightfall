from .player_base import Player
from player.skills.knight_skills import get_knight_skills

class Knight(Player):
    def __init__(self):
        super().__init__(name="Knight", attack=25, defense=5, health=100, type=1)
        self.all_skills = get_knight_skills(self)
        self.unlock_skills()
        