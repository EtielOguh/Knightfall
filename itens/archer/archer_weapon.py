from ..itens_base import Itens_Base
from ..rarity import Rarity

class WoodBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Wood Bow", attack=15, defense=0, type=2, rarity= Rarity.COMMON, price=price)

class StoneBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Stone Bow", attack=20, defense=0, type=2, rarity= Rarity.UNCOMMON, price=price)

class IronBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Iron Bow", attack=25, defense=0, type=2, rarity= Rarity.RARE, price=price)

class DiamondBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Diamond bow", attack=25, defense=0, type=2, rarity= Rarity.EPIC, price=price)
        
class HellfangBow(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Hellfang Bow", attack=25, defense=0, type=2, rarity= Rarity.DEVIL, price=price)
