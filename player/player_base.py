from random import randint
import rules
from time import sleep
from copy import deepcopy
from itens.stone import Stone

class Player():
    def __init__(self, player_name, health, attack, defense, type):
        self.name = player_name
        self.class_type = type
        self.level = 1
        self.attack = attack
        self.skills = []
        self.all_skills = []
        self.defense = defense
        self.health = health
        self.mana = 100
        self.mana_max = 100
        self.max_health = 100
        self.zone = 1
        self.right_hand = []
        self.left_hand = []
        self.head = []
        self.body = []
        self.hands = []
        self.bag = []
        self.healpotions = 0
        self.manapotions = 0
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
    
    def use_skill(self, skill_index, enemy):
        if skill_index < 0 or skill_index >= len(self.skills):
            print ("Invalid Skill!")
        
        skill = self.skills[skill_index]
        if self.mana >= skill["mana_cost"]:
            self.mana -= skill["mana_cost"]
            skill["execute"](enemy)
            print(f"Mana:{self.mana}/{self.mana_max}")
        else:
            print("No mana!")
            
    def unlock_skills(self):
        self.skills = [
            s for s in self.all_skills if self.level >= s["required_level"]
        ]
    
    def level_up(self):
            self.level += 1
            self.xp -= self.xp_max
            self.attack += 3
            self.max_health += 50
            self.mana_max += 20
            self.health = self.max_health
            self.mana = self.mana_max
            self.xp_max = self.calculate_xp_max(self.level)
            self.unlock_skills()
            print(f"Level Up! {self.level}. Xp Left: {self.xp}/{self.xp_max}")
    
    def stats(self):
        print(f"{self.name} Lv.{self.level}")
        print(f"HP {self.health}/{self.max_health} | MP {self.mana}/{self.mana_max}")
        print(f"ATK {self.attack} | DEF {self.defense}")
        print(f"XP {self.xp}/{self.xp_max} | $ {self.money}")

    
    def potion_drops(self):
        dropped = []
        drop_chance = randint(0, 9)

        if drop_chance == 9:
            self.healpotions += 1
            dropped.append("Heal Potion")

        elif drop_chance == 8:
            self.manapotions += 1
            dropped.append("Mana Potion")

        return dropped
            
    def show_bag_itens(self):
        for i, item in enumerate(self.bag, start=1):
            if hasattr(item, "buff"):
                print(f"{i}) {item.name} +{item.buff}")
            else:
                print(f"{i}) {item.name} x {item.quantity}")
                
    def show_equip_itens(self):
        equip_slots = {
            "Right Hand": self.right_hand,
            "Left Hand": self.left_hand,
            "Head": self.head,
            "Body": self.body,
            "Hands": self.hands
        }

        index = 1
        equip_map = {}

        for slot_name, slot_items in equip_slots.items():
            if slot_items:
                item = slot_items[0]
                equip_map[index] = item
                print(f"{index}) {slot_name}: {item.name} +{item.buff}")
                index += 1

        if not equip_map:
            print("No equipped items.")

        return equip_map

    def add_item_to_bag(self, item):
        # Só empilha se o item for empilhável (tem quantity) e for do mesmo tipo
        if hasattr(item, 'quantity') and hasattr(item, 'name'):
            for bag_item in self.bag:
                if (
                    bag_item.name == item.name
                    and getattr(bag_item, 'type', None) == getattr(item, 'type', None)
                ):
                    bag_item.quantity += item.quantity
                    if isinstance(item, Stone):
                        print(f"{item.quantity}x {item.name} stacked in your bag. Total: {bag_item.quantity}")
                    return

        # Caso contrário, adiciona como item separado
        self.bag.append(item)
        print(f"{item.name} x{getattr(item, 'quantity', 1)} added to your bag.")


    def exp_wins(self, monster):
        self.xp += monster.exp
        while self.xp >= self.xp_max:
            self.level_up()


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
        print("\n--- Currently Equipped Items ---")

        equipment_slots = {
            "Right Hand": self.right_hand,
            "Left Hand ": self.left_hand,
            "Armor     ": self.body,
            "Head      ": self.head
        }

        for slot_name, items_list in equipment_slots.items():
            item_name = items_list[0].name if items_list else "Empty"
            print(f"| {slot_name} | {item_name}")

        print("--------------------------------\n")
    


        if not self.bag:
            rules.clear()
            print("Empty Bag!\n")
            return

        # Filtra só itens que não são stones (joias)
        visible_items = [item for item in self.bag if not getattr(item, "is_stone", False)]

        if not visible_items:
            print("No equipable items in bag.\n")
            return

        print("\nBag Items:")
        for idx, item in enumerate(visible_items, 1):
                print(f"{idx}) Name: {item.name} | Attack: {item.base_attack} | Defence: {item.defense} | Quantity: x{item.quantity}")
        print("0) Cancel and go back")

        while True:
            try:
                choice = int(input("\nTell me the item number: "))

                if choice == 0:
                    print("Returning to the game...")
                    sleep(0.5)
                    rules.clear()
                    return

                if choice < 1 or choice > len(visible_items):
                    print("Invalid item number!")
                    continue

                selected_item = visible_items[choice - 1]

                # Se tem mais de 1 na pilha, tira 1 pra equipar
                if hasattr(selected_item, "quantity") and selected_item.quantity > 1:
                    selected_item.quantity -= 1
                    item_to_equip = deepcopy(selected_item)
                    item_to_equip.quantity = 1
                else:
                    item_to_equip = selected_item
                    self.bag.remove(selected_item)

                # Equipamentos por slots

                if item_to_equip.slot == "right_hand":
                    if self.right_hand:
                        old = self.right_hand.pop()
                        self.attack -= old.attack
                        self.defense -= old.defense
                        print(f"{old.name} broke!")
                    self.right_hand.append(item_to_equip)
                
                elif item_to_equip.slot == "left_hand":
                    if self.left_hand:
                        old = self.left_hand.pop()
                        self.attack -= old.attack
                        self.defense -= old.defense
                        print(f"{old.name} broke!")
                    self.left_hand.append(item_to_equip)
                
                elif item_to_equip.slot == "head":
                    if self.head:
                        old = self.head.pop()
                        self.attack -= old.attack
                        self.defense -= old.defense
                        print(f"{old.name} broke!")
                    self.head.append(item_to_equip)

                elif item_to_equip.slot == "body":
                    if self.body:
                        old = self.body.pop()
                        self.attack -= old.attack
                        self.defense -= old.defense
                        print(f"{old.name} broke!")
                    self.body.append(item_to_equip)
                
                else:
                    print(f"Cannot equip {item_to_equip.name}. Invalid slot.")
                    self.bag.append(item_to_equip)
                    break

                self.attack += item_to_equip.attack
                self.defense += item_to_equip.defense

            except ValueError:
                print("Please enter a valid number!")