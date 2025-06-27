from .stone import Stone

class JewelOfLive(Stone):
    def __init__(self, price = None):
        super().__init__(
            name="Jewel Of Life",
            type=3,
            quantity= 1,
            price = price,
            is_stone = True
        )
