import sys

from animation import battle_animation
from player.player_base import Player
from rules import spawn_monster, try_drop_item, clear, boss_fight, try_drop_stone
from merchants import merchant

from battle.combat_ui import CombatUI
from battle.battle_rewards import BattleRewards


class BattleSystem:
    def __init__(self, player):
        self.player = player
        self.monster = spawn_monster(player.zone, player)
        self.ui = CombatUI()
        self.rewards = BattleRewards(
            ui=self.ui,
            spawn_monster_func=spawn_monster,
            try_drop_stone_func=try_drop_stone,
            try_drop_item_func=try_drop_item
        )

    def start(self):
        while self.player.player_is_alive():
            while self.monster.enemy_is_alive() and self.player.player_is_alive():
                clear()
                print(self.monster.battle_cry())
                self.ui.show_status(self.player, self.monster)

                action = self.ui.show_main_battle_menu()

                if action == "a":
                    self.handle_auto_battle()

                elif action == "b":
                    self.handle_turn_battle()

                elif action == "p":
                    self.handle_potions()

                elif action == "f":
                    clear()
                    print("You ran away.\n")
                    self.monster = spawn_monster(self.player.zone, self.player)
                    break

                elif action == "m":
                    self.handle_full_menu()

                else:
                    print("Invalid action!")

    def handle_auto_battle(self):
        battle_animation()

        while self.monster.enemy_is_alive() and self.player.player_is_alive():
            self.player.attack_enemy(self.monster)

            if self.monster.enemy_is_alive():
                self.monster.attack_player(self.player)

            if self.player.health <= 20 or self.monster.attack > self.player.health:
                if self.player.healpotions > 0:
                    self.player.use_heal_potion()

        if not self.monster.enemy_is_alive():
            clear()
            self.monster = self.rewards.handle_monster_defeat(self.player, self.monster)

    def handle_turn_battle(self):
        clear()
        self.ui.event("You entered turn battle mode.", 0.5)

        result = self.turn_based_battle()

        if result:
            clear()
            self.monster = self.rewards.handle_monster_defeat(self.player, self.monster)
        else:
            self.monster = spawn_monster(self.player.zone, self.player)

    def turn_based_battle(self):
        while self.player.player_is_alive() and self.monster.enemy_is_alive():
            clear()
            self.ui.show_status(self.player, self.monster)

            action = self.ui.show_turn_menu()

            if action == "a":
                damage = self.player.attack_enemy(self.monster)
                self.ui.event(f"You dealt {damage} damage to {self.monster.name}.", 0.4)

                if self.monster.enemy_is_alive():
                    damage = self.monster.attack_player(self.player)
                    self.ui.event(f"{self.monster.name} dealt {damage} damage to you.", 0.5)

            elif action == "p":
                self.handle_potions()

            elif action == "f":
                self.ui.event("You ran away from battle.", 0.5)
                return False

            elif action == "s":
                self.handle_skills()

            else:
                self.ui.event("Invalid action.", 0.3)

        return True

    def handle_skills(self):
        print("\nSkills:")
        for index, skill in enumerate(self.player.skills):
            print(f"[{index}] {skill['name']} - Mana: {skill['mana_cost']} - {skill['description']}")

        try:
            choice = int(input("Choose your skill: "))
            self.player.use_skill(choice, self.monster)
        except ValueError:
            print("Invalid skill choice.")

    def handle_potions(self):
        choice = self.ui.show_potion_menu(self.player)

        if choice == "1":
            self.player.use_heal_potion()
        elif choice == "2":
            self.player.use_mana_potion()
        else:
            print("Invalid option.")

    def handle_full_menu(self):
        clear()
        action = self.ui.show_full_menu()

        if action == "z":
            if self.player.money >= 50 and self.player.change_zone():
                self.player.money -= 50
                clear()
                print(f"Now you are in Zone {self.player.zone} | -$50 | ${self.player.money} left!\n")
                self.monster = spawn_monster(self.player.zone, self.player)
            else:
                print("Cannot change zone.")

        elif action == "x":
            if self.player.money >= 50 and self.player.back_zone():
                self.player.money -= 50
                clear()
                print(f"Now you are in Zone {self.player.zone} | -$50 | ${self.player.money} left!\n")
                self.monster = spawn_monster(self.player.zone, self.player)
            else:
                print("Cannot go back zone.")

        elif action == "i":
            clear()
            Player.equip_items(self.player)

        elif action == "s":
            from player.save_manager import save_player
            save_player(self.player)
            sys.exit()

        elif action == "e":
            clear()
            self.player.show_bag_itens()

        elif action == "p":
            clear()
            boss = boss_fight(self.player.zone, self.player.level)
            if boss:
                self.monster = boss

        elif action == "d":
            clear()
            self.player.dynamic_zone = True
            self.monster = spawn_monster(self.player.zone, self.player)

        elif action == "h":
            clear()
            self.player.dynamic_zone = False
            self.monster = spawn_monster(self.player.zone, self.player)

        elif action == "m":
            merchant(self.player)

        elif action == "q":
            clear()