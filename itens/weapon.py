from itens_base import Itens

# -----------------------
# Armas para Archer (type = 2)
# -----------------------
class BowOfFire(Itens):
    def __init__(self):
        super().__init__(name="Bow of Fire", attack=15, defense=0, type=2)

class WindstrikerBow(Itens):
    def __init__(self):
        super().__init__(name="Windstriker Bow", attack=20, defense=1, type=2)

class ElvenLongbow(Itens):
    def __init__(self):
        super().__init__(name="Elven Longbow", attack=25, defense=0, type=2)

# -----------------------
# Armas para Knight (type = 1)
# -----------------------
class SwordOfValor(Itens):
    def __init__(self):
        super().__init__(name="Sword of Valor", attack=18, defense=2, type=1)

class IronGreatsword(Itens):
    def __init__(self):
        super().__init__(name="Iron Greatsword", attack=22, defense=1, type=1)

class BladeOfKings(Itens):
    def __init__(self):
        super().__init__(name="Blade of Kings", attack=30, defense=3, type=1)

# -----------------------
# Escudos para Knight (type = 1)
# -----------------------
class ShieldOfStone(Itens):
    def __init__(self):
        super().__init__(name="Shield of Stone", attack=0, defense=10, type=1)

class DragonShield(Itens):
    def __init__(self):
        super().__init__(name="Dragon Shield", attack=0, defense=15, type=1)

class AegisOfHonor(Itens):
    def __init__(self):
        super().__init__(name="Aegis of Honor", attack=0, defense=20, type=1)

# -----------------------
# Armas para Thief (type = 3)
# -----------------------
class DaggerOfNight(Itens):
    def __init__(self):
        super().__init__(name="Dagger of Night", attack=12, defense=2, type=3)

class SilentBlade(Itens):
    def __init__(self):
        super().__init__(name="Silent Blade", attack=17, defense=1, type=3)

class VenomfangDagger(Itens):
    def __init__(self):
        super().__init__(name="Venomfang Dagger", attack=20, defense=0, type=3)