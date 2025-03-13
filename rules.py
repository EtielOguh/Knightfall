from random import choice
from monsters import gosma, dragon, demon, goblin, angel

def spawn_monster(player):
        monster_class = choice([gosma.Gosma, dragon.Dragon, demon.Demon, goblin.Goblin, angel.Angel])
        return monster_class(player)