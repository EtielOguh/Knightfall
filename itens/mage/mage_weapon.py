from ..itens_base import Itens_Base
from ..rarity import Rarity

class WoodenWand(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Wooden Wand", attack=16, defense=0, type=4, rarity=Rarity.COMMON, price=price, buff=0, quantity=1)

class CrystalWand(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Crystal Wand", attack=22, defense=0, type=4, rarity=Rarity.UNCOMMON, price=price, buff=0, quantity=1)

class ArcaneStaff(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Arcane Staff", attack=30, defense=0, type=4, rarity=Rarity.RARE, price=price, buff=0, quantity=1)

class ElderStaff(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Elder Staff", attack=40, defense=0, type=4, rarity=Rarity.EPIC, price=price, buff=0, quantity=1)

class StaffOfTheVoid(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Staff of the Void", attack=55, defense=0, type=4, rarity=Rarity.DEVIL, price=price, buff=0, quantity=1)
