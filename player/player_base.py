from random import randint
import json
from enum import Enum
from itens.rarity import Rarity
import rules
from time import sleep

class Player():
    def __init__(self, name, health, attack, defense, type):
        self.name = name
        self.class_type = type
        self.level = 1
        self.attack = attack
        self.defense = defense
        self.health = health
        self.max_health = 100
        self.zone = 1
        self.right_hand = []
        self.left_hand = []
        self.bag = []
        self.potion = 0
        self.xp = 0
        self.xp_max = 100
        self.money = 0
        self.dynamic_zone = False

    def player_is_alive(self):
        return self.health > 0

    def damage_received(self, damage):
        self.health -= damage

    def attack_enemy(self, enemy):
        damage = randint(self.attack - 1, self.attack + 5)
        if damage > enemy.health:
            damage = enemy.health
        enemy.damage_received(damage)

    def stats(self):
        print(f"Player Stats: {self.name} Lv:{self.level} | HP:{self.health}/{self.max_health} | Atk:{self.attack} | Def:{self.defense} | XP:{self.xp}/{self.xp_max} | $:{self.money} | Pot: {self.potion}\n")

    def potion_drops(player):
        drop_chance = randint(0, 3)
        if drop_chance == 3:
            player.potion += 1
            print(f"Potion drops: + 1")

    def potion_use(player):
        if player.potion > 0 and player.health < player.max_health:
            heal_amount = min(40, player.max_health - player.health)
            player.health += heal_amount
            player.potion -= 1
            print(f"Potion used your HP now is: {player.health}/{player.max_health}")
        elif player.potion == 0:
            print("You don't have potion to use")

    def show_bag_itens(player):
        if not player.bag:
            print("Empty Bag!")
        else:
            print("Bag Itens: ")
            for item in player.bag:
                print(item, end="\n\n")

    def add_item_to_bag(self, item):
        self.bag.append(item)
        print(f"{item} added to your bag.")

    def exp_wins(self, monster):
        self.xp += monster.exp
        while self.xp >= self.xp_max:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_max
        self.attack += 3
        self.max_health += 50
        self.health = self.max_health
        self.xp_max = self.calculate_xp_max(self.level)
        print(f"Level Up! {self.level}. Xp Left: {self.xp}/{self.xp_max}")

    def calculate_xp_max(self, level):
        # Função nova progressiva para XP máximo
        return 30 + (level - 1) * 50 + int((level - 1)**2 * 10)

    def change_zone(self):
        if self.zone < 4:
            self.zone += 1
            return True
        else:
            return False

    def back_zone(self):
        if self.zone > 1:
            self.zone -= 1
            return True
        else:
            return False

    def equip_itens(self):
        print("Currently Equipped Items:")
    
        if self.right_hand:
            print(f"Right Hand: {self.right_hand[0]}")
        else:
            print("Right Hand: Empty")

        if self.left_hand:
            print(f"Left Hand: {self.left_hand[0]}")
        else:
            print("Left Hand: Empty")
            if not self.bag:
                rules.clear()
                print("Empty Bag!\n")
                return

        print("\nBag Items:")
        for idx, item in enumerate(self.bag, 1):
            print(f"{idx}) {item}")
        print("0) Cancel and go back")

        while True:
            try:
                choice = int(input("\nTell me the item number: ")) - 1

                if choice == -1:
                    print("Returning to the game...")
                    sleep(0.5)
                    rules.clear()
                    return

                if choice < 0 or choice >= len(self.bag):
                    print("Invalid item number!")
                    continue

                selected_item = self.bag[choice]

                if selected_item.attack > 0:
                    if self.right_hand:
                        old = self.right_hand.pop()
                        self.attack -= old.attack
                        self.defense -= old.defense
                        print(f"{old.name} broke.")
                    self.right_hand.append(selected_item)
                else:
                    if self.left_hand:
                        old = self.left_hand.pop()
                        self.attack -= old.attack
                        self.defense -= old.defense
                        print(f"{old.name} broke.")
                    self.left_hand.append(selected_item)

                self.attack += selected_item.attack
                self.defense += selected_item.defense
                self.bag.remove(selected_item)

                rules.clear()
                print(f"{selected_item.name} has been successfully equipped!")
                break

            except ValueError:
                print("Please enter a valid number!")