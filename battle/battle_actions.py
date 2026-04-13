from .log_types import LOG_COMBAT, LOG_SYSTEM, LOG_IMPORTANT

class BattleActions:
    def __init__(self, battle, ui):
        self.battle = battle
        self.ui = ui
        
    def attack(self):
        player = self.battle.player
        monster = self.battle.monster

        if not player.player_is_alive() or not monster.enemy_is_alive():
            return

        damage = player.attack_enemy(monster)
        self.ui.trigger_enemy_hit_effect()
        self.ui.add_log(f"{player.name} dealt {damage} damage to {monster.name}.", LOG_COMBAT)

        if monster.enemy_is_alive():
            enemy_damage = monster.attack_player(player)
            self.ui.trigger_player_hit_effect()
            self.ui.add_log(f"{monster.name} dealt {enemy_damage} damage to {player.name}.", LOG_COMBAT)
            self.ui.add_floating_text(f"-{damage}", 760, 210, color=(255, 90, 90))
            self.ui.add_floating_text(f"-{enemy_damage}", 180, 210, color=(255, 90, 90))
        else:
            self.battle.monster = self.battle.rewards.handle_monster_defeat(player, monster)
            self.ui.sync_entities()
            self.ui.add_log(f"A new {self.battle.monster.name} appeared.", LOG_IMPORTANT)
            self.ui.show_battle_cry()

    def run(self):
        self.ui.add_log("You ran away.", LOG_IMPORTANT)
        self.battle.run_from_battle()
        self.ui.sync_entities()
        self.ui.show_battle_cry()

    def use_bag_item(self, item):
        player = self.battle.player

        if isinstance(item, dict):
            if item["kind"] == "heal_potion":
                if player.healpotions > 0:
                    player.use_heal_potion()
                    self.ui.add_log("Heal Potion used.", LOG_COMBAT)
                else:
                    self.ui.add_log("No Heal Potion left.", LOG_COMBAT)
                return

            if item["kind"] == "mana_potion":
                if player.manapotions > 0:
                    player.use_mana_potion()
                    self.ui.add_log("Mana Potion used.", LOG_COMBAT)
                else:
                    self.ui.add_log("No Mana Potion left.", LOG_COMBAT)
                return

        self.ui.add_log(f"{item.name} cannot be used in battle.", LOG_SYSTEM)

    def try_equip_item(self, item):
        if hasattr(item, "slot"):
            self.battle.player.equip_item(item)
            self.ui.add_log(f"{item.name} equipped.", LOG_SYSTEM)
        else:
            self.ui.add_log(f"{item.name} cannot be equipped.", LOG_SYSTEM)

    def use_skill(self, skill_index):
        player = self.battle.player
        monster = self.battle.monster

        if not player.player_is_alive() or not monster.enemy_is_alive():
            return

        result = player.use_skill(skill_index, monster)

        if not result["success"]:
            if result["reason"] == "invalid_skill":
                self.ui.add_log("Invalid skill.", LOG_SYSTEM)
            elif result["reason"] == "no_mana":
                self.ui.add_log("Not enough mana.", LOG_SYSTEM)
            return

        skill = result["skill"]
        damage = result["damage"]

        self.ui.add_log(f"{player.name} used {skill['name']} for {damage} damage.", LOG_COMBAT)
        self.ui.add_floating_text(f"-{damage}", 760, 210, color=(255, 90, 90))
        self.ui.trigger_enemy_hit_effect(duration=12, flash_duration=8, shake_intensity=12)
        self.ui.add_floating_text(f"-{damage}", 760, 210, color=(255, 90, 90))

        if monster.enemy_is_alive():
            enemy_damage = monster.attack_player(player)
            self.ui.add_log(f"{monster.name} dealt {enemy_damage} damage to {player.name}.", LOG_COMBAT)
            self.ui.add_floating_text(f"-{enemy_damage}", 180, 210, color=(255, 90, 90))
            self.ui.trigger_player_hit_effect()
        else:
            self.battle.monster = self.battle.rewards.handle_monster_defeat(player, monster)
            self.ui.sync_entities()
            self.ui.add_log(f"A new {self.battle.monster.name} appeared.", LOG_IMPORTANT)
            self.ui.show_battle_cry()