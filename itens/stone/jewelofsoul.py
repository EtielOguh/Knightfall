from .stone import Stone

class JewelofSoul(Stone):
    def __init__(self, price = None):
        super().__init__(
            name="Jewel of Soul",
            type=1,
            quantity= 0,
            price = price,
            is_stone = True
        )
