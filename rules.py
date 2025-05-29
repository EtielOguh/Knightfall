from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
from random import choice, randint
from player.knight import Knight
from player.thief import Thief
from player.archer import Archer
from player.player_base import Player
import os

from itens.weapon import *


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

def load_or_create_player():
    if os.path.exists("save_data.json"):
        try:
            player = Player.load_player()
            print(f"\n✅ Jogador {player.name} carregado com sucesso!")
            return player
        except Exception as e:
            print(f"\n❌ Erro ao carregar o save: {e}")
            print("Criando novo jogador...")
    else:
        print("Nenhum save encontrado. Criando novo jogador...")

    return chose_class()

def get_droppable_items(player_type):
    if player_type == 1:  # Knight
        return [SwordOfValor(), IronGreatsword(), BladeOfKings(),
                ShieldOfStone(), DragonShield(), AegisOfHonor()]
    elif player_type == 2:  # Archer
        return [BowOfFire(), WindstrikerBow(), ElvenLongbow()]
    elif player_type == 3:  # Thief
        return [DaggerOfNight(), SilentBlade(), VenomfangDagger()]
    return []
    
def try_drop_item(player):
    chance = randint(0, 3)  # 25% de chance
    if chance == 3:
        items = get_droppable_items(player.class_type)
        dropped_item = choice(items)
        player.add_item_to_bag(dropped_item)
        print(f"Lucky! Item Found: {dropped_item.name}")
