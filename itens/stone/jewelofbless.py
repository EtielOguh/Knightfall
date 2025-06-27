from .stone import Stone
from ..rarity import Rarity

class JewelofBless(Stone):
    def __init__(self):
        super().__init__(
            name="Jewel Of Bless",
            type=2,
            quantity= 1
        )
