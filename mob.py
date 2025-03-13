from random import randint, choice

class Enemy():
    def __init__(self,name, level, attack, health, max_health):
        self.name = name
        self.level = level
        self.attack = attack
        self.health = health
        self.max_health = max_health

    def enemy_is_alive(self):
        return self.health > 0
    
    def damage_received(self, damage):
        self.health -= damage
        print(f"{self.name} received {damage} damage HP LEFT {self.health}/{self.max_health}")
        
    def attack_player(self, player):
        damage = randint (self.attack -1, self.attack +5)
        if damage > player.health:
            damage = player.health
        player.damage_received(damage)
    
class Gosma(Enemy):
    def __init__(self, player):
        name = "Gosma"
        level = randint(player.level, player.level + 1)
        attack = randint(0, 6)
        max_health = randint(player.max_health // 2, player.max_health)
        health = max_health 

        super().__init__(name, level, attack, health, max_health)

        print(f"{self.name} is gonna kill you! {self.health}/{self.max_health}")
        
class Dragon(Enemy):
    def __init__(self, player):
        name = "Dragon"
        level = randint(player.level, player.level + 1)
        attack = randint(0, 6)
        max_health = randint(player.max_health // 2, player.max_health)
        health = max_health  
        

        super().__init__(name, level, attack, health, max_health)

        print(f"{self.name} is gonna kill you! {self.health}/{self.max_health}")
        
        
        
def spawn_monster(player):
    monster_class = choice([Gosma, Dragon]) #Escolhendo aleatório
    return monster_class(player)