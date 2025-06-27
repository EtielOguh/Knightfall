from random import randint

class Stone():
    def __init__(self,name, type, quantity,is_stone, price = None):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.price = price if price is not None else self.gerar_preco()
        self.is_stone = is_stone
        
        
    def gerar_preco(self):
        return randint(20, 40)
    
    def __str__(self):
        return f"{self.name} x{self.quantity}"