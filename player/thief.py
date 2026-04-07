from .player_base import Player
from player.skills.thief_skills import get_thief_skills

class Thief(Player):
    def __init__(self, player_name):
        super().__init__(player_name=player_name, attack=20, defense=3, health=90, type=3, class_name="Thief")
        self.all_skills = get_thief_skills(self)
        self.unlock_skills()