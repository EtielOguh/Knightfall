class Stone():
    def __init__(self,name, type, quantity):
        self.name = name
        self.type = type
        self.quantity = quantity
        
    def __str__(self):
        return f"{self.name}"