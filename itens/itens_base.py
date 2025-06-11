from random import randint

class Itens_Base:
    def __init__(self, name, attack, defense, type, rarity, price=None):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.type = type
        self.rarity = rarity
        self.price = price if price is not None else self.gerar_preco()

    def gerar_preco(self):
        return randint(20, 40)

    def __str__(self):
        return f"{self.name} (ATK: {self.attack} | DEF: {self.defense} | RARITY: {self.rarity.name} | PRICE: R$ {self.price})"
