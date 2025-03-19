from random import randint

class Player():
    def __init__(self):
        self.name = "Knight"
        self.level = 1
        self.attack = 10   
        self.health = 100
        self.max_health = 100
        self.zone = 1
        self.right_hand = []
        self.left_hand = []
        self.bag = ["Itens", "Exemple"]
        self.potion = 0
        self.xp = 0
        self.xp_max = 30
    
    def player_is_alive(self):
        return self.health > 0
    
    def damage_received(self, damage):
        self.health -= damage
        #print(f"{self.name} received {damage} damage HP LEFT {self.health}/{self.max_health}")
        
    def attack_enemy(self, enemy):
        damage = randint (self.attack -1, self.attack +5)
        if damage > enemy.health:
            damage = enemy.health
        enemy.damage_received(damage)
    
    def stats(self):
        print(f"\n{self.name} - level {self.level}")
        print(f"HP: {self.health}/{self.max_health} | Attack: {self.attack}\n")
        print(f"XP {self.xp}/{self.xp_max}")


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
            
    def show_bag_itens(player):
        print(player.bag)
    
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
        self.xp_max = self.calculate_new_exp_max() 

        print(f"Parabéns! Você subiu para o nível {self.level}. XP restante: {self.xp}/{self.xp_max}")
    
    def calculate_new_exp_max(self):
        return self.xp_max + 50
    
    def change_zone(self):
        if self.zone <4:
            self.zone += 1
            print(f"You have changed your zone, now your in {self.zone}")
        else:
            print("You can't change your zone!")