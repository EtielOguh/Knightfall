from random import randint
import json
from itens.weapon import (
    BowOfFire, WindstrikerBow, ElvenLongbow,
    SwordOfValor, IronGreatsword, BladeOfKings,
    ShieldOfStone, DragonShield, AegisOfHonor,
    DaggerOfNight, SilentBlade, VenomfangDagger
)
item_classes = {
    "Bow of Fire": BowOfFire,
    "Windstriker Bow": WindstrikerBow,
    "Elven Longbow": ElvenLongbow,
    "Sword of Valor": SwordOfValor,
    "Iron Greatsword": IronGreatsword,
    "Blade of Kings": BladeOfKings,
    "Shield of Stone": ShieldOfStone,
    "Dragon Shield": DragonShield,
    "Aegis of Honor": AegisOfHonor,
    "Dagger of Night": DaggerOfNight,
    "Silent Blade": SilentBlade,
    "Venomfang Dagger": VenomfangDagger
}

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
        self.xp_max = 30
        self.money = 0
    
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
        print(f"MONEY R$ {self.money}")

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
        for item in player.bag:
            print(item)
    
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
        self.xp_max = self.calculate_new_exp_max() 

        print(f"Parabéns! Você subiu para o nível {self.level}. XP restante: {self.xp}/{self.xp_max}")
    
    def calculate_new_exp_max(self):
        return self.xp_max + 50
    
    def change_zone(self):
        if self.zone <4:
            self.zone += 1
            print(f"You have changed your zone, now your in {self.zone}")
            return True
        else:
            print("You can't change your zone!")
            return False
        
    def back_zone(self):
        if self.zone > 1:
            self.zone -= 1
            print(f"You have changed your zone, now your in {self.zone}")
            return True
        else:
            print("You can't change your zone!")
            return False
    
    def equip_itens(self):
        if not self.bag:
            print("Sua bag está vazia!")
            return
        
        print("\nItens na sua bag:")
        for item in self.bag:
            print(item)
        item = self.bag[int(input("\nDigite o Número do item: "))]


        for item in self.bag[:]:  # Usa uma cópia da lista para evitar problemas ao remover
            # Decide se vai para mão direita (tem ataque) ou esquerda (escudo)
            if item.attack > 0:
                if self.right_hand:
                    old = self.right_hand.pop() if self.right_hand else None
                    self.attack -= old.attack
                    self.defense -= old.defense
                    print(f"{old.name} foi quebrado.")
                self.right_hand.append(item)
            else:
                if self.left_hand:
                    old = self.left_hand.pop() if self.left_hand else None
                    self.attack -= old.attack
                    self.defense -= old.defense
                    print(f"{old.name} foi quebrado.")
                self.left_hand.append(item)

            # Aplica atributos do novo item
            self.attack += item.attack
            self.defense += item.defense
            self.bag.remove(item)
            print(f"{item.name} foi equipado com sucesso!")
            return  # Equipa só um item e sai do método

        print("Item não encontrado na bag.")


    def to_dict(self):
        return {
            "name": self.name,
            "class_type": self.class_type,
            "level": self.level,
            "attack": self.attack,
            "defense": self.defense,
            "health": self.health,
            "max_health": self.max_health,
            "zone": self.zone,
            "xp": self.xp,
            "xp_max": self.xp_max,
            "money": self.money,
            "potion": self.potion,
            "bag": [vars(item) for item in self.bag],
            "right_hand": [vars(item) for item in self.right_hand],
            "left_hand": [vars(item) for item in self.left_hand]
        }

    @staticmethod
    def save_player(player, filename="save_data.json"):
        with open(filename, "w") as f:
            json.dump(player.to_dict(), f, indent=4)

    @staticmethod
    def load_player(filename="save_data.json"):
        with open(filename, "r") as f:
            data = json.load(f)

        from player.knight import Knight
        from player.archer import Archer
        from player.thief import Thief

        if data["class_type"] == 1:
            player = Knight()
        elif data["class_type"] == 2:
            player = Archer()
        elif data["class_type"] == 3:
            player = Thief()

        player.name = data["name"]
        player.level = data["level"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        player.health = data["health"]
        player.max_health = data["max_health"]
        player.zone = data["zone"]
        player.xp = data["xp"]
        player.xp_max = data["xp_max"]
        player.money = data["money"]
        player.potion = data["potion"]

        player.bag = [item_classes[i["name"]]() for i in data["bag"]]
        player.right_hand = [item_classes[i["name"]]() for i in data["right_hand"]]
        player.left_hand = [item_classes[i["name"]]() for i in data["left_hand"]]

        return player