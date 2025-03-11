from mob import Enemy
from knight import Player
from time import sleep

def Battle():
    player = Player()
    print(f"Wellcome to the jungle! {player.name}!")

    while player.player_is_alive():
        monster = Enemy.create_enemy(player)
        while Enemy.enemy_is_alive(monster) and player.player_is_alive():
            action = input("A for Attack and B for potion: ")
            if action in 'aA':
                while Enemy.enemy_is_alive(monster) and player.player_is_alive():
                    player.attack_enemy(monster)
                    sleep(1)
                    if Enemy.enemy_is_alive(monster):
                        Enemy.attack_player(monster,player)
                    if not Enemy.enemy_is_alive(monster):
                        print(f'{monster.name} Defeated!')
                        player.potion_drops()
                        break
            elif action in "bB":
                player.potion_use()
                        
                    