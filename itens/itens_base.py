class Itens_Base():
    def __init__(self, name, attack, defense, type):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.type = type
        
    def __str__(self):
        return f"{self.name} (ATK: {self.attack} | DEF: {self.defense})"
        