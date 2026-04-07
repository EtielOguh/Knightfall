from itens.stone import Jewel_group

STONE_BY_TYPE = {
    1: [],
    2: [],
    3: []
}

for stone_class in Jewel_group:
    STONE_BY_TYPE[stone_class().type].append(stone_class)