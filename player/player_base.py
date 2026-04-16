from random import randint
import rules
from copy import deepcopy
from itens.stone import Stone

class Player():
    def __init__(self, player_name, health, attack, defense, type, class_name):
        self.name = player_name
        self.class_type = type
        self.class_name = class_name
        self.level = 1
        self.attack = attack
        self.skills = []
        self.all_skills = []
        self.defense = defense
        self.health = health
        self.mana = 100
        self.mana_max = 100
        self.max_health = health
        self.zone = 1
        self.right_hand = []
        self.left_hand = []
        self.head = []
        self.body = []
        self.hands = []
        self.foot = []
        self.bag = []
        self.healpotions = 0
        self.manapotions = 0
        self.xp = 0
        self.xp_max = 100
        self.money = 0
        self.player_hit_timer = 0
        self.player_flash_timer = 0
        self.player_shake_intensity = 0
        

    def player_is_alive(self):
        return self.health > 0

    def damage_received(self, damage):
        self.health -= damage

    def attack_enemy(self, enemy):
        damage = randint(self.attack - 1, self.attack + 5)
        if damage > enemy.health:
            damage = enemy.health
        enemy.damage_received(damage)

        return damage
    
    def use_skill(self, skill_index, enemy):
        if skill_index < 0 or skill_index >= len(self.skills):
            return {"success": False, "reason": "invalid_skill"}

        skill = self.skills[skill_index]

        if self.mana < skill["mana_cost"]:
            return {"success": False, "reason": "no_mana", "skill": skill}

        previous_enemy_hp = enemy.health
        previous_player_hp = self.health
        previous_player_mana = self.mana

        self.mana -= skill["mana_cost"]
        skill["execute"](enemy)

        damage = max(0, previous_enemy_hp - enemy.health)
        healed = max(0, self.health - previous_player_hp)
        mana_spent = max(0, previous_player_mana - self.mana)

        return {
            "success": True,
            "skill": skill,
            "damage": damage,
            "healed": healed,
            "mana_spent": mana_spent,
            "mana": self.mana,
            "mana_max": self.mana_max
        }
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
    
    def use_heal_potion(self):
        if self.healpotions <= 0:
            return False

        if self.health >= self.max_health:
            return False

        heal_amount = 50
        self.healpotions -= 1
        self.health = min(self.max_health, self.health + heal_amount)
        return True


    def use_mana_potion(self):
        if self.manapotions <= 0:
            return False

        if self.mana >= self.mana_max:
            return False

        mana_amount = 30
        self.manapotions -= 1
        self.mana = min(self.mana_max, self.mana + mana_amount)
        return True
            
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
        if isinstance(item, type):
            raise ValueError(f"Expected an item instance, got class: {item.__name__}")

        is_stackable = hasattr(item, "quantity") and hasattr(item, "name")

        if is_stackable:
            for bag_item in self.bag:
                same_class = bag_item.__class__ == item.__class__
                same_type = getattr(bag_item, "type", None) == getattr(item, "type", None)

                if same_class and same_type:
                    bag_item.quantity += item.quantity
                    return {
                        "action": "stacked",
                        "item": bag_item,
                        "added_quantity": item.quantity,
                        "total_quantity": bag_item.quantity
                    }

        self.bag.append(item)
        return {
            "action": "added",
            "item": item,
            "added_quantity": getattr(item, "quantity", 1)
        }


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


    def equip_item(self, selected_item):
        if selected_item is None:
            return False, "Invalid item."

        if getattr(selected_item, "is_stone", False):
            return False, f"{selected_item.name} cannot be equipped."

        slot_map = {
            "right_hand": self.right_hand,
            "left_hand": self.left_hand,
            "head": self.head,
            "body": self.body
        }

        target_slot = slot_map.get(getattr(selected_item, "slot", None))

        if target_slot is None:
            return False, f"Cannot equip {selected_item.name}. Invalid slot."

        if selected_item not in self.bag:
            return False, f"{selected_item.name} is not in bag."

        if hasattr(selected_item, "quantity") and selected_item.quantity > 1:
            selected_item.quantity -= 1
            item_to_equip = deepcopy(selected_item)
            item_to_equip.quantity = 1
        else:
            item_to_equip = selected_item
            self.bag.remove(selected_item)

        if target_slot:
            old_item = target_slot.pop()
            self.attack -= getattr(old_item, "attack", 0)
            self.defense -= getattr(old_item, "defense", 0)
            self.bag.append(old_item)

        target_slot.append(item_to_equip)
        self.attack += getattr(item_to_equip, "attack", 0)
        self.defense += getattr(item_to_equip, "defense", 0)

        return True, f"Equipped: {item_to_equip.name}"
    
    def trigger_player_hit_effect(self, duration=10, flash_duration=6, shake_intensity=8):
        self.player_hit_timer = duration
        self.player_flash_timer = flash_duration
        self.player_shake_intensity = shake_intensity

    #------------------------#
    #Penalidades de lvl
    #------------------------#

    def level_down(self):
        if self.level <= 1:
            self.level = 1
            self.xp = 0
            self.xp_max = self.calculate_xp_max(self.level)
            self.unlock_skills()
            return False

        self.level -= 1
        self.attack = max(self.base_attack, self.attack - 3)
        self.max_health = max(self.base_max_health, self.max_health - 50)
        self.mana_max = max(self.base_mana_max, self.mana_max - 20)

        self.health = min(max(1, self.health), self.max_health)
        self.mana = min(self.mana, self.mana_max)

        self.xp_max = self.calculate_xp_max(self.level)
        self.unlock_skills()
        return True

    def preview_death_penalty(self, loss_percent=0.20):
        xp_loss = max(1, int(self.xp_max * loss_percent))
        will_level_down = self.level > 1 and self.xp < xp_loss

        return {
            "xp_loss": xp_loss,
            "loss_percent": int(loss_percent * 100),
            "current_level": self.level,
            "will_level_down": will_level_down,
        }

    def apply_death_penalty(self, loss_percent=0.20):
        xp_loss = max(1, int(self.xp_max * loss_percent))
        remaining_loss = xp_loss
        old_level = self.level

        while remaining_loss > 0:
            if self.xp >= remaining_loss:
                self.xp -= remaining_loss
                remaining_loss = 0
                break

            remaining_loss -= self.xp
            self.xp = 0

            if self.level == 1:
                break

            self.level_down()
            self.xp = self.xp_max

        if self.level == 1 and self.xp < 0:
            self.xp = 0

        return {
            "xp_loss": xp_loss,
            "old_level": old_level,
            "new_level": self.level,
            "level_down": self.level < old_level,
        }