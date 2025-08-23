from rules import spawn_monster, try_drop_item, clear, boss_fight, merchant, try_drop_stone
from player.player_base import Player
from animation import battle_animation
from player.save_manager import save_player
import sys
from time import sleep


def show_full_menu():
    valid = ['z', 'x', 'i', 's', 'e', 'p', 'd', 'h', 'm', 'q']
    print("\n=== Full Menu ===")
    print("Z) Next Zone (-$50)   X) Back Zone (-$50)   I) Equip Items")
    print("S) Save and Exit   E) Show Bag   P) Boss Fight   D) Enable Dynamic Zone")
    print("H) Disable Dynamic Zone   M) Merchant   Q) Back to Battle\n")
    choice = input("Choose your option: ").lower()
    return choice

def show_battle_menu():
    print("\n====================== Battle Menu =======================")
    print("A) Attack   F) Runaway   P) Use Potion   M) Open Full Menu")
    print("B) Enter Battle Mode (Turn-Based)")
    print("==========================================================")
    return input("Choose your action: ").lower()

def print_battle_status(player, monster):
    print("=" * 70)
    print(f"| {'PLAYER STATS':^32} | {'MONSTER STATS':^32} |")
    print("-" * 70)
    print(f"| {'Name: ' + player.name:<32} | {'Name: ' + monster.name:<32} |")
    print(f"| {'Level: ' + str(player.level):<32} | {'Level: ' + str(monster.level):<32} |")
    print(f"| {'HP: ' + f'{player.health}/{player.max_health}':<32} | {'HP: ' + f'{monster.health}/{monster.max_health}':<32} |")
    print(f"| {'Mana: ' + f'{player.mana}/{player.mana_max}':<32} | {'Damage: ' + str(monster.attack):<32} |")
    print(f"| {'Damage: ' + str(player.attack):<32} | {'':<32} |")
    print("=" * 70)
    print(f"| {'INVENTORY AND MORE':^66}  |")
    print("-" * 70)
    print(f"| {'HP POTIONS: ' + str(player.healpotions):<32} | {'MANA POTIONS: ' + str(player.manapotions):<32} |")
    print(f"| {'XP: ' + f'{player.xp}/{player.xp_max}':<32} | {'Zone: ' + str(player.zone):<32} |")
    print("=" * 70)


    
def turn_based_battle(player, monster):
    while player.player_is_alive() and monster.enemy_is_alive():
        clear()
        print_battle_status(player, monster)
        print("\nA) Attack   P) Potion   F) Run  S)Skill Damage")
        action = input("> ")

        if action == 'a':
            dmg = player.attack_enemy(monster)
            print(f"\nYou hit {monster.name} for {dmg} damage!")

            if monster.enemy_is_alive():
                mdmg = monster.attack_player(player)
                print(f"{monster.name} hits you for {mdmg} damage!")
                    
        elif action == 'p':
            print("Which potion:")
            print("[1] Heal Potion")
            print("[2] Mana Potion")
            choice = input("Choice: ")

            if choice == '1':
                player.use_heal_potion()
                sleep(1)
            elif choice == '2':
                player.use_mana_potion()
                sleep(1)
            else:
                print("Invalid Option")

        elif action == 'f':
            print("You ran away from the battle!\n")
            return False
        
        elif action == 's':
            print("Skills: ")
            for i, s in enumerate (player.skills):
                print(f"{i + 1}) {s['name']} - Mana: {s['mana_cost']} - {s['description']}")
            
            skill_choice = int(input("Choose your skill: "))
            player.use_skill(skill_choice - 1, monster)
            sleep(1)
            
        else:
            print("Invalid action!")

    return True

def Battle(player):
    monster = spawn_monster(player.zone, player)

    while player.player_is_alive():
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
                        if player.healpotions > 0:
                            player.use_healpotions()

                if not monster.enemy_is_alive():
                    clear()
                    save_player(player)
                    print(f"{monster.name} Defeated!")
                    player.exp_wins(monster)
                    monster.drop_money(player)
                    player.potion_drops()
                    try_drop_stone(monster, player)
                    try_drop_item(player, monster)
                    monster = spawn_monster(player.zone, player)

            elif action == 'b':
                clear()
                print("You enter full Battle Mode!\n")
                result = turn_based_battle(player, monster)
                if result:
                    print(f"{monster.name} defeated!\n")
                    player.exp_wins(monster)
                    monster.drop_money(player)
                    player.potion_drops()
                    try_drop_stone(monster, player)
                    try_drop_item(player, monster)
                    save_player(player)
                    monster = spawn_monster(player.zone, player)
                else:
                    monster = spawn_monster(player.zone, player)

            elif action == 'f':
                clear()
                print('LOSER! Try another one!\n')
                monster = spawn_monster(player.zone, player)
                break

            elif action == 'p':
                clear()
                print("Which potion:")
                print("[1] Heal Potion")
                print("[2] Mana Potion")
                choice = input("Choice: ")

                if choice == '1':
                    player.use_heal_potion()
                elif choice == '2':
                    player.use_mana_potion()
                else:
                    print("Invalid Option")

            elif action == 'm':
                clear()
                full_action = show_full_menu()

                if full_action == 'z':
                    if player.money >= 50:
                        player.money -= 50
                        if player.change_zone():
                            clear()
                            print(f"Now you are in Zone! {player.zone} | -$50 Bucks ${player.money} Left!\n")
                            monster = spawn_monster(player.zone, player)
                        else:
                            print("You don't have enough money!\n")

                elif full_action == 'x':
                    if player.money >= 50:
                        if player.back_zone():
                            player.money -= 50
                            clear()
                            print(f"Now you are in Zone! {player.zone} | -$50 Bucks ${player.money} Left!\n")
                            monster = spawn_monster(player.zone, player)
                        else:
                            print("You can't change your zone!\n")
                    else:
                        print("You don't have enough money!\n")

                elif full_action == 'i':
                    clear()
                    Player.equip_itens(player)

                elif full_action == 's':
                    save_player(player)
                    sys.exit()

                elif full_action == 'e':
                    clear()
                    player.show_bag_itens()

                elif full_action == 'p':
                    clear()
                    boss = boss_fight(player.zone, player.level)
                    if boss:
                        monster = boss
                    else:
                        print("No boss fight started.\n")

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

            else:
                print("Invalid action!")


