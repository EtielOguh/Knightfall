from rules import spawn_monster, try_drop_item, clear, boss_fight, merchant
from player.player_base import Player
from animation import battle_animation
from player.save_manager import save_player
import sys


def show_battle_menu():
    valid = ['a', 'f', 'p', 'm']
    while True:
        print("\n=== Battle Menu ===")
        print("A) Attack   F) Runaway   P) Use Potion   M) Open Full Menu\n")
        choice = input("Choose your action: ").lower()
        if choice in valid:
            return choice
        clear()
        print("Invalid action! Try again.")


def show_full_menu():
    valid = ['z', 'x', 'i', 's', 'e', 'p', 'd', 'h', 'm', 'q']
    while True:
        print("\n=== Full Menu ===")
        print("Z) Next Zone (-$50)   X) Back Zone (-$50)   I) Equip Items")
        print("S) Save and Exit   E) Show Bag   P) Boss Fight   D) Enable Dynamic Zone")
        print("H) Disable Dynamic Zone   M) Merchant   Q) Back to Battle\n")
        choice = input("Choose your option: ").lower()
        if choice in valid:
            return choice
        clear()
        print("Invalid action! Try again.")


def Battle(player):
    clear()
    print(f"Here is where your story begin! {player.name}!\n")

    while player.player_is_alive():
        monster = spawn_monster(player.zone, player)

        while monster.enemy_is_alive() and player.player_is_alive():
            player.stats()
            print(monster.battle_cry())
            action = show_battle_menu()

            if action == 'a':
                battle_animation()

                while monster.enemy_is_alive() and player.player_is_alive():
                    player.attack_enemy(monster)

                    if monster.enemy_is_alive():
                        monster.attack_player(player)
                    if player.health <= 20 or monster.attack > player.health:
                        if player.potion > 0:
                            player.potion_use()

                if not monster.enemy_is_alive():
                    clear()
                    save_player(player)
                    print(f"\n{monster.name} Defeated!")
                    player.exp_wins(monster)
                    monster.drop_money(player)
                    player.potion_drops()
                    try_drop_item(player, monster)

            elif action == 'f':
                clear()
                print('LOSER! Try another one!\n')
                monster = spawn_monster(player.zone, player)

            elif action == 'p':
                clear()
                player.potion_use()

            elif action == 'm':
                clear()
                full_action = show_full_menu()
                
                if full_action == 'z':
                    change = False
                    if player.money >= 50:
                        player.money -= 50
                        change = player.change_zone()
                    if change:
                        clear()
                        print(f"Now you are in Zone! {player.zone} | -$50 Bucks ${player.money} Left!\n")
                        monster = spawn_monster(player.zone, player)
                        print(monster.battle_cry())
                    else:
                        clear()
                        print("You don't have enough money!\n")

                elif full_action == 'x':
                    if player.money < 50:
                        print("You don't have enough money!\n")
                    else:
                        change = player.back_zone()
                        if change:
                            player.money -= 50
                            clear()
                            print(f"Now you are in Zone! {player.zone} | -$50 Bucks ${player.money} Left!\n")
                            monster = spawn_monster(player.zone, player)
                            print(monster.battle_cry())
                        else:
                            clear()
                            print("You can't change your zone!\n")

                elif full_action == 'i':
                    clear()
                    Player.equip_itens(player)

                elif full_action == 's':
                    save_player()
                    sys.exit()

                elif full_action == 'e':
                    clear()
                    player.show_bag_itens()

                elif full_action == 'p':
                    clear()
                    monster = boss_fight(player.zone)

                elif full_action == 'd':
                    clear()
                    player.dynamic_zone = True
                    monster = spawn_monster(player.zone, player)

                elif full_action == 'h':
                    clear()
                    player.dynamic_zone = False
                    monster = spawn_monster(player.zone, player)

                elif full_action == 'm':
                    merchant(player)

                elif full_action == 'q':
                    clear()
                    # volta para menu rápido sem fazer nada

            else:
                print("Invalid action!")
