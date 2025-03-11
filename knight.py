from random import randint
from mob import Enemy

class Player():
    def __init__(self):
        self.name = "Knight"
        self.level = 1
        self.attack = 800   
        self.health = 100
        self.max_health = 100
        self.right_hand = []
        self.left_hand = []
        self.bag = []
        self.potion = 0
    
    def player_is_alive(self):
        return self.health > 0
    
    def damage_received(self, damage):
        self.health -= damage
        print(f"{self.name} received {damage} damage HP LEFT {self.health}/{self.max_health}")
        
    def attack_enemy(self, enemy):
        damage = randint (self.attack -1, self.attack +5)
        if damage > enemy.health:
            damage = enemy.health
        enemy.damage_received(damage)
    
    def stats(self):
        print(f"\n{self.name} - level {self.level}")
        print(f"HP: {self.health}/{self.max_health} | Attack: {self.attack}\n")


    def potion_drops(player):
        drop_chance = randint(0,3)
        if drop_chance == 3:
            player.potion += 1
            print (f"Potion drops: {player.potion}")

    def potion_use(player):
        if player.potion > 0 and player.health < player.max_health:
            heal_amount = min(40, player.max_health - player.health)  
            player.health += heal_amount
            player.potion -= 1 
            print (f"Potion used your HP now is: {player.health}/{player.max_health}")
        elif player.potion == 0:
            print("You don't have potion to use")