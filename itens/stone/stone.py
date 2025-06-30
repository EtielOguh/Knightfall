def gerar_preco(type):
        return (10 * type)
    
class Stone():
    def __init__(self,name, type, quantity,is_stone, price = None):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.price = price if price is not None else gerar_preco(type)
        self.is_stone = is_stone
    
    
    def __str__(self):
        return f"{self.name} (QUANTITY: {self.quantity} | PRICE: {self.price})"