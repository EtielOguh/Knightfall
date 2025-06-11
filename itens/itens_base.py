class Itens_Base():
    def __init__(self, name, attack, defense, type, rarity, price):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.type = type
        self.rarity = rarity
        self.price = price
        
    def __str__(self):
        return f"{self.name} (ATK: {self.attack} | DEF: {self.defense} | RARITY: {self.rarity.name} | PRICE: R$ {self.price})"
        