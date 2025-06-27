from .stone import Stone

class JewelofBless(Stone):
    def __init__(self, price = None):
        super().__init__(
            name="Jewel Of Bless",
            type=2,
            quantity= 1,
            price = price,
            is_stone = True
        )
