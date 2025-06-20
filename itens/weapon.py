from .itens_base import Itens_Base
from .rarity import Rarity
from random import randint
# -----------------------
# Armas para Knight (type = 1)
# -----------------------
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

# -----------------------
# Escudos para Knight (type = 1)
# -----------------------
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

# -----------------------
# Armas para Archer (type = 2)
# -----------------------
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

# -----------------------
# Armas para Thief (type = 3)
# -----------------------
class WoodDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Wood Dagger", attack=12, defense=0, type=3, rarity= Rarity.COMMON, price=price)

class StoneDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Stone Dagger", attack=17, defense=0, type=3, rarity= Rarity.UNCOMMON, price=price)

class IronDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Iron Dagger", attack=20, defense=0, type=3, rarity= Rarity.RARE, price=price)

class DiamondDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Diamond Dagger", attack=20, defense=0, type=3, rarity= Rarity.EPIC, price=price)

class HellspireDagger(Itens_Base):
    def __init__(self,price= None):
        super().__init__(name="Hellspire Dagger", attack=20, defense=0, type=3, rarity= Rarity.DEVIL, price=price)