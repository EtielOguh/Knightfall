from random import randint

class Itens_Base:
    def __init__(self, name, attack, defense, type, rarity, buff,quantity, price = None):
        self.name = name
        self.base_attack = attack
        self.defense = defense
        self.type = type
        self.rarity = rarity
        self.buff = buff
        self.quantity = quantity
        self.price = price if price is not None else self.gerar_preco()

    def gerar_preco(self):
        return randint(20, 40)
    
    @property
    def attack(self):
        multiplicadores = {
            0: 1.0,
            1: 1.2,
            2: 1.4,
            3: 1.6,
            4: 1.8,
            5: 2.0,
            6: 2.3,
            7: 2.6,
            8: 3.0,
            9: 3.5
        }
        multiplicador = multiplicadores.get(self.buff, 1.0)
        return int(self.base_attack * multiplicador)
    


    def __str__(self):
        return f"{self.name} (ATK: {self.attack} | DEF: {self.defense} | RARITY: {self.rarity.name} | PRICE: R$ {self.price} | QUANTITY: {self.quantity})"

