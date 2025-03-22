import random

class Item:
    def __init__(self, name, item_type, effect, drop_chance):
        self.name = name
        self.item_type = item_type  # Example: "potion", "weapon", "shield"
        self.effect = effect  # Example: {"health": 20} for a healing potion
        self.drop_chance = drop_chance  # Chance (0-100) of dropping
        
    def __str__(self):
        return f"{self.name} ({self.item_type}) - Effect: {self.effect} | Drop Chance: {self.drop_chance}%"
