from random import randint
from mob import Enemy

class Player():
    def __init__(self):
        self.name = "Knight"
        self.level = 1
        self.attack = 10   
        self.health = 100
        self.max_health = 100
    
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
    
    def exibir_status(self):
        """Mostra as informações do jogador"""
        print(f"\n{self.name} - Nível {self.level}")
        print(f"Vida: {self.health}/{self.max_health} | Ataque: {self.attack}\n")