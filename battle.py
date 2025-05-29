from rules import spawn_monster, try_drop_item
from player.player_base import Player
from animation import battle_animation
import sys

def Battle(player):
    print(f"Welcome to the jungle, {player.name}!")

    while player.player_is_alive():
        monster = spawn_monster(player.zone)
        print(monster.battle_cry())

        while monster.enemy_is_alive() and player.player_is_alive():
            action = input("\nChoose an action:\n[A] Attack\n[B] Use Potion\n[Z] Change Zone\n[X] Back Zone\n[F] Run Enemy\n[I] Equip Iten\n> ").strip().lower()
            
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
                    print(f"\n{monster.name} Defeated!")
                    player.exp_wins(monster)
                    monster.drop_money(player)
                    player.potion_drops()
                    try_drop_item(player)
                    print("\nPlayer Stats:")
                    player.stats()
                    player.show_bag_itens()

            elif action == 'b':
                player.potion_use()
                
            elif action == 'z':
                change = False  # Inicializa a variável para evitar erro
                if player.money >= 50:
                    player.money -= 50
                    change = player.change_zone()
                if change:
                    monster = spawn_monster(player.zone)
                    print(monster.battle_cry())
                else:
                    print("You don't have enough money!")

            elif action == 'x':
                change = False  # Mesma correção aqui
                if player.money >= 50:
                    player.money -= 50
                    change = player.back_zone()
                if change:
                    monster = spawn_monster(player.zone)
                    print(monster.battle_cry())
                else:
                    print("You don't have enough money!")
            
            elif action == 'f':
                print('LOSER! Try another one!')
                monster = spawn_monster(player.zone)
                print(monster.battle_cry())
            elif action == 'i':
                Player.equip_itens(player)
                  
            elif action == 's':
                Player.save_player(player)
                sys.exit()
            
            else:
                print("Invalid action!")                
                