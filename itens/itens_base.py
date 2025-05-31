class Itens_Base():
    def __init__(self, name, attack, defense, type, rarity):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.type = type
        self.rarity = rarity
        
    def __str__(self):
        return f"{self.name} (ATK: {self.attack} | DEF: {self.defense} | RARITY: {self.rarity})"
        