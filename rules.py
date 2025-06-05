from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
from monsters.boss import boss_zone
from random import choice, randint
from player.knight import Knight
from player.thief import Thief
from player.archer import Archer
from player.player_base import Player
import os
from itens.weapon import *

def boss_fight():
    return choice(boss_zone)()
    
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
    print("+-----------------------------+")
    print("|      CHOOSE YOUR CLASS      |")
    print("+-----------------------------+")
    print("| 1 – Knight                  |")
    print("| 2 – Archer                  |")
    print("| 3 – Thief                   |")
    print("+-----------------------------+")
    
    choice = input("> Escolha (1, 2 ou 3): ").strip()

    if choice == "1":
        player = Knight()
    elif choice == "2":
        player = Archer()
    elif choice == "3":
        player = Thief()
    else:
        print("Invalid, now your class is a Knight for base")
        player = Knight()
        
    return player

def load_or_create_player():
    if os.path.exists("save_data.json"):
        try:
            player = Player.load_player()
            print(f"\n✅ Jogador {player.name} carregado com sucesso!")
            return player
        except Exception as e:
            print(f"\n❌ Error! You don't have a save: {e}")
            print( "Creating a new player...")
    else:
        print( "No save found, creating a new player...")

    return chose_class()

def get_droppable_items(player, mob):
    # Lista de itens por classe
    items_by_class = {
        1: [WoodSwoord(), StoneSword(), IronSword(), DiamondSword(), DragonSlayerSword(),
            WoodShield(), StoneShield(), IronShield(), DiamondShield()],     # Knight
        2: [WoodBow(), StoneBow(), IronBow(), DiamondBow(), HellfangBow()],        # Archer
        3: [WoodDagger(), StoneDagger(), IronDagger(), DiamondBow(), HellspireDagger()]     # Thief
    }

    # Filtra os itens que têm raridade permitida no mob
    droppable_items = [
        item for item in items_by_class.get(player.class_type, [])
        if item.rarity in mob.allowed_rarities
    ]

    return droppable_items
    
def try_drop_item(player, mob):
    chance = randint(0, 3)  # 25% de chance
    if chance == 3:
        possible_items = get_droppable_items(player, mob)
        if possible_items:
            dropped_item = choice(possible_items)
            player.add_item_to_bag(dropped_item)
            print(f"Lucky! {mob.name} dropped: {dropped_item.name}")
        else:
            print(f"{mob.name} didn't drop anything suitable for your class.")

def show_menu():
    print("\nA) Attack     B) Potion     Z) Change     X) Back")
    print("F) Run        I) Equip      E) Bag        S) Save/Exit")
    action = input("Choose one > ").strip().lower()
    return action

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')