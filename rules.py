from monsters.zona1 import monster_zona1
from monsters.zona2 import monster_zona2
from monsters.zona3 import monster_zona3
from monsters.zona4 import monster_zona4
from monsters.Infinityzone import monster_dynamic
from monsters.boss import boss_zone_1, boss_zone_2,boss_zone_3, boss_zone_4
from random import choice, randint
from player.knight import Knight
from player.thief import Thief
from player.archer import Archer
from player.player_base import Player
import os
from itens.weapon import *
from time import sleep

def boss_fight(zone):
    if zone ==1:
        return choice(boss_zone_1)()
    elif zone ==2:
        return choice(boss_zone_2)()
    elif zone == 3:
        return choice(boss_zone_3)()
    elif zone == 4:
        return choice (boss_zone_4)()
    else:
        return ("Invalid Zone")
    
    
def spawn_monster(zone, player):
    if player.dynamic_zone == True:
       return choice(monster_dynamic)(player.level)
    elif zone == 1:
        return choice(monster_zona1)()
    elif zone == 2:
        return choice(monster_zona2)()
    elif zone == 3:
        return choice(monster_zona3)()
    elif zone == 4:
        return choice(monster_zona4)()
    else:
        raise ValueError("Invalid Zone")

def chose_class():
    print("1 – Knight | 2 – Archer | 3 – Thief")
    choice = input("> Choose (1, 2, or 3): ").strip()

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
    from random import randint

    rarities_with_chances = {
        Rarity.DEVIL: 0.5,
        Rarity.EPIC: 1,
        Rarity.RARE: 3,
        Rarity.UNCOMMON: 5,
        Rarity.COMMON: 10
    }

    possible_items = get_droppable_items(player, mob)

    if not possible_items:
        print(f"{mob.name} didn't drop anything suitable for your class.")
        return

    for rarity, chance in rarities_with_chances.items():
        roll = randint(1, 1000)  # escala maior pra permitir 0.5%
        if roll <= chance * 10:  # ex: 0.5% vira 5 em 1000
            items_of_rarity = [item for item in possible_items if item.rarity == rarity]
            if items_of_rarity:
                dropped_item = choice(items_of_rarity)
                player.add_item_to_bag(dropped_item)
                print(f"Lucky! {mob.name} dropped: {dropped_item.name} ({rarity.name})")
                return

    print(f"{mob.name} didn't drop anything this time.")

def show_menu():
    print("\nA) Attack Enemy     B) Potion     Z) Change Zone   X) Back Zone   D) Dynamic Zone ON     P) Boss Fight")
    print("F) Run Enemy       I) Equip Iten     E) Show Bag        S) Save/Exit    H) Dynamic Zone OFF")
    action = input("Choose one > ").strip().lower()
    return action

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def merchant(self):
    print("\nBag Items:")
    for idx, item in enumerate(self.bag, 1):
        print(f"{idx}) {item}")
    print("0) Cancel and go back")

    while True:
        try:
            choice = int(input("\ntell me the item you want to sell: ")) - 1

            if choice == -1:
                print ("Returning to the game...")
                clear()
                return
            if choice < 0 or choice >= len(self.bag):
                print("Invalid number!")
                continue

            selected_item = self.bag[choice]

            money_gained = selected_item.price
            self.money += money_gained

            self.bag.pop(choice)

            print(f"You sold {selected_item.name} for R$ {selected_item.price} ")
            print(f"Current money R$ {self.money}")

            if len(self.bag) > 0:
                out = input("Do you want to sell more itens: [y|n]")
                if out == 'y':
                    continue
                if out == "n":
                    break
                else:
                    print("Invalid option, returning to the game...")
                    sleep(0.3)
                    break
            else:
                print ("You don't have itens do sell. Returning to the game...")
                sleep(0.3)
                break

        except ValueError:
            print("Please Choose a right option!")
