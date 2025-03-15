from rules import spawn_monster
from knight import Player
from animation import battle_animation

def Battle():
    player = Player()
    print(f"Welcome to the jungle, {player.name}!")
    player.show_bag_itens()

    while player.player_is_alive():
        monster = spawn_monster(player.zone)
        print(monster.battle_cry())

        while monster.enemy_is_alive() and player.player_is_alive():
            action = input("\nChoose an action:\n[A] Attack\n[B] Use Potion\n[Z] Change Zone\n> ").strip().lower()
            
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
                    player.potion_drops()
                    print("\nPlayer Stats:")
                    player.stats()

            elif action == 'b':
                player.potion_use()
                
            elif action == 'z':
                player.change_zone()
            else:
                print("Invalid action! Please choose 'A' to Attack or 'B' to Use Potion.")
