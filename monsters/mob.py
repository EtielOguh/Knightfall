from random import randint

class Enemy():
    def __init__(self,name, level, attack, health, max_health, allowed_rarities):
        self.name = name
        self.level = level
        self.attack = attack
        self.health = health
        self.max_health = max_health
        self.exp = 10 * level
        self.allowed_rarities = allowed_rarities

    def enemy_is_alive(self):
        return self.health > 0
    
    def damage_received(self, damage):
        self.health -= damage
        
    def attack_player(self, player):
        damage = randint (self.attack -1, self.attack +5)
        if damage > player.health:
            damage = player.health
        player.damage_received(damage)
    
    def drop_money(self, player):
        money = self.level * 10
        player.money += money
    
    