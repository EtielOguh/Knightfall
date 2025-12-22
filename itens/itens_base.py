from random import randint
from .rarity import Rarity
from .rulesbuff import can_buff, apply_buff
rarity_multiplier = {
        Rarity.COMMON : 1.0,
        Rarity.UNCOMMON: 1.5,
        Rarity.RARE: 2.5,
        Rarity.EPIC: 3.5,
        Rarity.DEVIL: 5.0
    }
class Itens_Base:
    def __init__(self, name, attack, defense, type, rarity, buff,quantity, slot, price = None):
        self.name = name
        self.base_attack = attack
        self.defense = defense
        self.type = type
        self.rarity = rarity
        self.buff = buff
        self.slot = slot
        self.quantity = quantity
        self.price = price if price is not None else self.gerar_preco()


    def gerar_preco(self):
        base_value = 50
        multiplier = rarity_multiplier.get(self.rarity, 1.0)
        return base_value * multiplier

    def buff_equipped_items(player):
        while True:
            equip_map = player.show_equip_itens()
            print("0) Cancel and Back")

            if not equip_map:
                return

            try:
                choice = int(input("\nChoose equipped item to buff: "))

                if choice == 0:
                    return

                if choice not in equip_map:
                    print("Invalid choice!")
                    continue

            except ValueError:
                print("Wrong number, try again")
                continue

            item = equip_map[choice]

            if not can_buff(item):
                print("This item cannot be buffed.")
                continue

            apply_buff(item)
            print(f"{item.name} has been buffed! Now it is +{item.buff} 🔥")

    

    def buff_itens(player):
        while True:
            if not player.bag:
                print("You don't have itens")
                return
            
            player.show_bag_itens()
            print("0) Cancel and Back")

            try:
                choice = int(input("\nChoose one item to buff:")) - 1

                if choice == -1:
                    return
                    
                if choice < 0 or choice >= len(player.bag):
                    print("Invalid number! Try again!")
                    continue

            except ValueError:
                print ("Wrong number, try again")

            item = player.bag[choice]

            if not can_buff(item):
                print("This item cannot be buffed! Sorry")
                continue

            apply_buff(item)
            print(f"{item.name} has been buffed! now your item is lvl {item.buff}")

    @property
    def attack(self):
        multiplicadores = {
            0: 1.0,
            1: 1.2,
            2: 1.4,
            3: 1.6,
            4: 1.8,
            5: 2.0,
            6: 2.3,
            7: 2.6,
            8: 3.0,
            9: 3.5
        }
        
        multiplicador = multiplicadores.get(self.buff, 1.0)
        return int(self.base_attack * multiplicador)
    



    def __str__(self):
        return f"{self.name} (ATK: {self.attack} | DEF: {self.defense} | RARITY: {self.rarity.name} | PRICE: R$ {self.price} | QUANTITY: {self.quantity})"

