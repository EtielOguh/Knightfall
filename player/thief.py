from .player_base import Player
from player.skills.thief_skills import get_thief_skills

class Thief(Player):
    def __init__(self):
        super().__init__(name="Thief", attack=20, defense=3, health=90, type=3)
        self.all_skills = get_thief_skills(self)
        self.unlock_skills()