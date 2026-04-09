from .player_base import Player
from player.skills.mage_skills import get_mage_skills

class Mage(Player):
    def __init__(self, player_name):
        super().__init__(player_name=player_name, attack=25, defense=2, health=100, type=4, class_name="Mage")
        self.all_skills = get_mage_skills(self)
        self.unlock_skills()