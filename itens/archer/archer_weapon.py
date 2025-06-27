from ..itens_base import Itens_Base
from ..rarity import Rarity

class WoodBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Wood Bow", attack=15, defense=0, type=2, rarity= Rarity.COMMON, price=price, buff=0, quantity=1)

class StoneBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Stone Bow", attack=20, defense=0, type=2, rarity= Rarity.UNCOMMON, price=price, buff=0, quantity=1)

class IronBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Iron Bow", attack=25, defense=0, type=2, rarity= Rarity.RARE, price=price, buff=0, quantity=1)

class DiamondBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Diamond bow", attack=25, defense=0, type=2, rarity= Rarity.EPIC, price=price, buff=0, quantity=1)
        
class HellfangBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Hellfang Bow", attack=25, defense=0, type=2, rarity= Rarity.DEVIL, price=price, buff=0, quantity=1)
