from ..itens_base import Itens_Base
from ..rarity import Rarity

class LeatherHelmet(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Leather Helmet", attack=0, defense=10, type=0, rarity=Rarity.COMMON, price=price, buff=0,slot="head",category="helmet", quantity=1)

class IronHelmet(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Iron Helmet", attack=0, defense=18, type=0, rarity=Rarity.UNCOMMON, price=price, buff=0,slot="head",category="helmet", quantity=1)

class SteelHelmet(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Steel Helmet", attack=0, defense=25, type=0, rarity=Rarity.RARE, price=price, buff=0,slot="head",category="helmet", quantity=1)

class MithrilHelm(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Mithril Helm", attack=0, defense=35, type=0, rarity=Rarity.EPIC, price=price, buff=0,slot="head",category="helmet",  quantity=1)

class HelmetOfTheTitans(Itens_Base):
    def __init__(self, price=None):
        super().__init__(name="Helmet of the Titans", attack=0, defense=50, type=0, rarity=Rarity.DEVIL, price=price, buff=0,slot="head",category="helmet", quantity=1)