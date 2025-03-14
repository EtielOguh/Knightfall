from mob import Enemy
from rules import spawn_monster
from knight import Player
from animation import battle_animation


def Battle():
    player = Player()
    print(f"Wellcome to the jungle! {player.name}!")
    player.show_bag_itens()

    while player.player_is_alive():
        monster = spawn_monster(player)
        print(monster.battle_cry())
        
        while Enemy.enemy_is_alive(monster) and player.player_is_alive():
            action = input("A for Attack and B for potion: ")
            if action in 'aA':
                battle_animation()
                while Enemy.enemy_is_alive(monster) and player.player_is_alive():
                    player.attack_enemy(monster)
                    if Enemy.enemy_is_alive(monster):
                        monster.attack_player(player)
                    if not Enemy.enemy_is_alive(monster):
                        print(f'{monster.name} Defeated!')
                        player.exp_wins(monster)
                        player.potion_drops()
                        print("Stats player:")
                        player.stats()
                        
                        break
            elif action in "bB":
                player.potion_use()