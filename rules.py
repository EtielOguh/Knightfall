from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
from random import choice
from player.knight import Knight
from player.thief import Thief
from player.archer import Archer

def spawn_monster(zone):
    if zone == 1:
        return choice(monster_zona1)()
    elif zone == 2:
        return choice(monster_zona2)()
    elif zone == 3:
        return choice(monster_zona3)()
    elif zone == 4:
        return choice(monster_zona4)()
    else:
        raise ValueError("Invalid zone")
    
def chose_class():
    choice = input("Escolha sua classe (1-Knight, 2-Archer, 3-Thief): ")

    if choice == "1":
        player = Knight()
    elif choice == "2":
        player = Archer()
    elif choice == "3":
        player = Thief()
    else:
        print("Escolha inválida, criando Knight por padrão.")
        player = Knight()
        
    return player