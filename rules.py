from random import choice
from monsters import gosma, dragon, demon

def spawn_monster(player):
    monster_class = choice([gosma.Gosma, dragon.Dragon,demon.Demon]) #Escolhendo aleatório
    return monster_class(player)