from ..itens_base import Itens_Base
from ..rarity import Rarity

class LeatherArmor(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Leather Armor", attack=0, defense=15, type=0, rarity=Rarity.COMMON, price=price, buff=0, slot="body", category="armor", quantity=1)

class ChainmailArmor(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Chainmail Armor", attack=0, defense=25, type=0, rarity=Rarity.UNCOMMON, price=price, buff=0, slot="body", category="armor", quantity=1)

class PlateArmor(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Plate Armor", attack=0, defense=35, type=0, rarity=Rarity.RARE, price=price, buff=0, slot="body", category="armor", quantity=1)

class MithrilPlate(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Mithril Plate", attack=0, defense=45, type=0, rarity=Rarity.EPIC, price=price, buff=0, slot="body", category="armor", quantity=1)

class ArmorOfTheAncients(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Armor of the Ancients", attack=0, defense=60, type=0, rarity=Rarity.DEVIL, price=price, buff=0, slot="body", category="armor", quantity=1)