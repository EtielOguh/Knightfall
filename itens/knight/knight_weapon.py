from ..itens_base import Itens_Base
from ..rarity import Rarity

# Knight Swords

class WoodSwoord(Itens_Base):
    def __init__(self, price = None):
        super().__init__(name="Wood Sword", attack=18, defense=0, type=1, rarity= Rarity.COMMON, price=price)

class StoneSword(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Stone Sword", attack=22, defense=0, type=1,rarity= Rarity.UNCOMMON, price=price)

class IronSword(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Iron Sword", attack=30, defense=0, type=1, rarity= Rarity.RARE, price=price)

class DiamondSword(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Diamond Sword", attack=30, defense=0, type=1, rarity= Rarity.EPIC, price=price)

class DragonSlayerSword(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Dragon Slayer Sword", attack=30, defense=0, type=1, rarity= Rarity.DEVIL, price=price)
        
# Knight Shields

class WoodShield(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Wood Shield", attack=0, defense=10, type=1, rarity= Rarity.COMMON, price=price)

class StoneShield(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Stone Shiled", attack=0, defense=15, type=1, rarity= Rarity.UNCOMMON, price=price)

class IronShield(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Iron Shield", attack=0, defense=20, type=1, rarity= Rarity.RARE, price=price)

class DiamondShield(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Diamond Shield", attack=0, defense=20, type=1, rarity= Rarity.EPIC, price=price)

class MasterMindShield(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Master Mind Shield", attack=0, defense=0, type=1, rarity= Rarity.DEVIL, price=price)