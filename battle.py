from mob import Enemy
from knight import Player

def Battle():
    player = Player()
    print(f"Wellcome to the jungle! {player.name}!")

    while player.player_is_alive():
        Enemy.create_enemy(player)
        while Enemy.enemy_is_alive() and player.player_is_alive():
            player.attack_enemy()