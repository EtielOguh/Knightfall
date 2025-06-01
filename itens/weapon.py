from .itens_base import Itens_Base
from .rarity import Rarity

# -----------------------
# Armas para Knight (type = 1)
# -----------------------
class SwordOfValor(Itens_Base):
    def __init__(self):
        super().__init__(name="Sword of Valor", attack=18, defense=0, type=1, rarity= Rarity.COMMON)

class IronGreatsword(Itens_Base):
    def __init__(self):
        super().__init__(name="Iron Greatsword", attack=22, defense=0, type=1,rarity= Rarity.COMMON)

class BladeOfKings(Itens_Base):
    def __init__(self):
        super().__init__(name="Blade of Kings", attack=30, defense=0, type=1, rarity= Rarity.COMMON)

# -----------------------
# Escudos para Knight (type = 1)
# -----------------------
class ShieldOfStone(Itens_Base):
    def __init__(self):
        super().__init__(name="Shield of Stone", attack=0, defense=10, type=1, rarity= Rarity.COMMON)

class DragonShield(Itens_Base):
    def __init__(self):
        super().__init__(name="Dragon Shield", attack=0, defense=15, type=1, rarity= Rarity.COMMON)

class AegisOfHonor(Itens_Base):
    def __init__(self):
        super().__init__(name="Aegis of Honor", attack=0, defense=20, type=1, rarity= Rarity.COMMON)

# -----------------------
# Armas para Archer (type = 2)
# -----------------------
class BowOfFire(Itens_Base):
    def __init__(self):
        super().__init__(name="Bow of Fire", attack=15, defense=0, type=2, rarity= Rarity.COMMON )

class WindstrikerBow(Itens_Base):
    def __init__(self):
        super().__init__(name="Windstriker Bow", attack=20, defense=0, type=2, rarity= Rarity.COMMON)

class ElvenLongbow(Itens_Base):
    def __init__(self):
        super().__init__(name="Elven Longbow", attack=25, defense=0, type=2, rarity= Rarity.COMMON)

# -----------------------
# Armas para Thief (type = 3)
# -----------------------
class DaggerOfNight(Itens_Base):
    def __init__(self):
        super().__init__(name="Dagger of Night", attack=12, defense=0, type=3, rarity= Rarity.COMMON)

class SilentBlade(Itens_Base):
    def __init__(self):
        super().__init__(name="Silent Blade", attack=17, defense=0, type=3, rarity= Rarity.COMMON)

class VenomfangDagger(Itens_Base):
    def __init__(self):
        super().__init__(name="Venomfang Dagger", attack=20, defense=0, type=3, rarity= Rarity.COMMON)