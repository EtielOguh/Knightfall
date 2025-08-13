from .player_base import Player
from player.skills.archer_skills import get_archer_skills

class Archer(Player):
    def __init__(self):
        super().__init__(name="Archer", attack=30, defense=3, health=100, type=2)
        self.all_skills = get_archer_skills(self)
        self.unlock_skills()