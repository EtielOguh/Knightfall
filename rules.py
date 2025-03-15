from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
from random import choice

def spawn_monster(zone):
    if zone == 1:
        return choice(monsters_zone1)()
    elif zone == 2:
        return choice(monsters_zone2)()
    elif zone == 3:
        return choice(monsters_zone3)()
    elif zone == 3:
        return choice(monsters_zone4)()
    else:
        raise ValueError("Invalid zone")