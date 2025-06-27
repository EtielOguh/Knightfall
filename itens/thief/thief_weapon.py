from ..itens_base import Itens_Base
from ..rarity import Rarity


class WoodDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Wood Dagger", attack=12, defense=0, type=3, rarity= Rarity.COMMON, price=price, buff=0, quantity=1)

class StoneDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Stone Dagger", attack=17, defense=0, type=3, rarity= Rarity.UNCOMMON, price=price, buff=0, quantity=1)

class IronDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Iron Dagger", attack=20, defense=0, type=3, rarity= Rarity.RARE, price=price, buff=0, quantity=1)

class DiamondDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Diamond Dagger", attack=20, defense=0, type=3, rarity= Rarity.EPIC, price=price, buff=0, quantity=1)

class HellspireDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Hellspire Dagger", attack=20, defense=0, type=3, rarity= Rarity.DEVIL, price=price, buff=0, quantity=1)