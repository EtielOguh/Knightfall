class Item:
    def __init__(self, name, item_type, effect, drop_chance):
        self.name = name
        self.item_type = item_type
        self.effect = effect 
        self.drop_chance = drop_chance 

    def __str__(self):
        return f"{self.name} ({self.item_type}) - Effect: {self.effect} | Drop Chance: {self.drop_chance}%"
