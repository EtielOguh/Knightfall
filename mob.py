from random import randint, choice

class Enemy():
    def __init__(self,name, level, attack, health, max_health):
        self.name = name
        self.level = level
        self.attack = attack
        self.health = health
        self.max_health = max_health
        self.exp = 10 * level

    def enemy_is_alive(self):
        return self.health > 0
    
    def damage_received(self, damage):
        self.health -= damage
        #print(f"{self.name} received {damage} damage HP LEFT {self.health}/{self.max_health}")
        
    def attack_player(self, player):
        damage = randint (self.attack -1, self.attack +5)
        if damage > player.health:
            damage = player.health
        player.damage_received(damage)