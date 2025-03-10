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
        print(f"{self.name} received {damage} damage")
        
    def attack_player(self, player):
        damage = randint (self.attack -1, self.attack +5)
        if damage > player.health:
            damage = player.health
        player.damage_received(damage)
        
    def create_enemy(player):
        
        enemy_names = ["Goblin", "Orc", "Esqueleto", "Lobo Sombrio", "Bandido", "Zumbi", "Mago Negro"]
        name = choice(enemy_names)
        
        level = randint(player.level, player.level + 1)
        attack = randint(player.attack // 2, player.attack)
        max_health = randint(player.max_health // 2, player.max_health)
        health = max_health

        new_enemy = Enemy(name, level, attack, health, max_health)
        print(f" {name} Spawn (Lvl {level}, ATK {attack}, HP {health}/{max_health})")

        return new_enemy

    
    