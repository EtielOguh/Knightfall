from .player_base import Player
from player.skills.knight_skills import get_knight_skills

class Knight(Player):
    def __init__(self, player_name):
        super().__init__(player_name = player_name, attack=25, defense=5, health=100, type=1, class_name="Knight")
        self.all_skills = get_knight_skills(self)
        self.unlock_skills()
        