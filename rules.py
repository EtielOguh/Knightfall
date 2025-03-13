from random import choice
from monsters import gosma, dragon, demon, goblin, angel

def spawn_monster(player):
    if player.level == 1:
        monster_class = choice([gosma.Gosma, dragon.Dragon])
    elif player.level >= 2:
        monster_class = choice([demon.Demon, goblin.Goblin, angel.Angel])
    return monster_class(player)