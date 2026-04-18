from .log_types import LOG_COMBAT, LOG_SYSTEM, LOG_IMPORTANT
from battle.status_effects import process_status_effects, try_apply_status


class BattleActions:
    def __init__(self, battle, ui):
        self.battle = battle
        self.ui = ui

    def attack(self):
        if not self.battle.is_player_turn():
            return

        player = self.battle.player
        monster = self.battle.monster

        if not self.resolve_start_of_player_turn():
            return

        damage = player.attack_enemy(monster)
        self.ui.trigger_enemy_hit_effect()
        self.ui.add_log(f"{player.name} dealt {damage} damage to {monster.name}.", LOG_COMBAT)
        self.ui.add_floating_text(f"-{damage}", 760, 210, color=(255, 90, 90))

        try_apply_status(player, monster, self.ui)

        self.resolve_after_player_action()

    def use_skill(self, skill_index):
        if not self.battle.is_player_turn():
            return

        player = self.battle.player
        monster = self.battle.monster

        if not self.resolve_start_of_player_turn():
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

        try_apply_status(player, monster, self.ui)

        self.resolve_after_player_action()

    def use_bag_item(self, item):
        if not self.battle.is_player_turn():
            return

        player = self.battle.player

        if not self.resolve_start_of_player_turn():
            return

        used = False

        if isinstance(item, dict):
            if item["kind"] == "heal_potion":
                if player.healpotions > 0:
                    if player.use_heal_potion():
                        self.ui.add_log("Heal Potion used.", LOG_COMBAT)
                        used = True
                    else:
                        self.ui.add_log("Cannot use Heal Potion now.", LOG_SYSTEM)
                else:
                    self.ui.add_log("No Heal Potion left.", LOG_SYSTEM)

                if used:
                    self.resolve_after_player_action()
                return

            if item["kind"] == "mana_potion":
                if player.manapotions > 0:
                    if player.use_mana_potion():
                        self.ui.add_log("Mana Potion used.", LOG_COMBAT)
                        used = True
                    else:
                        self.ui.add_log("Cannot use Mana Potion now.", LOG_SYSTEM)
                else:
                    self.ui.add_log("No Mana Potion left.", LOG_SYSTEM)

                if used:
                    self.resolve_after_player_action()
                return

        self.ui.add_log(f"{item.name} cannot be used in battle.", LOG_SYSTEM)

    def try_equip_item(self, item):
        if not self.battle.is_player_turn():
            return

        success, message = self.battle.player.equip_item(item)
        self.ui.add_log(message, LOG_SYSTEM if success else LOG_IMPORTANT)

    def run(self):
        if not self.battle.is_player_turn():
            return

        self.ui.add_log("You ran away.", LOG_IMPORTANT)
        self.battle.run_from_battle()
        self.ui.sync_entities()
        self.ui.show_battle_cry()

    def resolve_start_of_player_turn(self):
        player = self.battle.player
        monster = self.battle.monster

        if not player.player_is_alive() or not monster.enemy_is_alive():
            return False

        status_result = process_status_effects(player, self.ui)

        if status_result["damage_taken"] > 0:
            self.ui.add_floating_text(
                f"-{status_result['damage_taken']}",
                180,
                190,
                color=(170, 255, 120)
            )

        if not player.player_is_alive():
            self.handle_player_defeat()
            return False

        return True

    def resolve_start_of_enemy_turn(self):
        player = self.battle.player
        monster = self.battle.monster

        if not player.player_is_alive() or not monster.enemy_is_alive():
            return False

        status_result = process_status_effects(monster, self.ui)

        if status_result["damage_taken"] > 0:
            self.ui.add_floating_text(
                f"-{status_result['damage_taken']}",
                760,
                190,
                color=(170, 255, 120)
            )

        if not monster.enemy_is_alive():
            self.handle_monster_defeat()
            return False

        return True

    def resolve_after_player_action(self):
        player = self.battle.player
        monster = self.battle.monster

        if not monster.enemy_is_alive():
            self.handle_monster_defeat()
            return

        if not player.player_is_alive():
            self.handle_player_defeat()
            return

        current_time = self.ui.get_time()
        self.battle.schedule_enemy_turn(current_time)

    def enemy_take_turn(self):
        if not self.battle.is_enemy_turn():
            return

        if not self.battle.pending_enemy_action:
            return

        player = self.battle.player
        monster = self.battle.monster

        if not player.player_is_alive() or not monster.enemy_is_alive():
            self.battle.clear_enemy_turn_schedule()
            return

        self.battle.clear_enemy_turn_schedule()

        if not self.resolve_start_of_enemy_turn():
            return

        action = monster.decide_action(player)
        action_type = action.get("type", "attack")
        label = action.get("label", "Attack")

        if action_type == "guard":
            monster.guard_active = True
            self.ui.add_log(f"{monster.name} used {label} and braced for impact.", LOG_COMBAT)

        elif action_type == "double_attack":
            total_damage = 0

            for _ in range(2):
                if not player.player_is_alive():
                    break

                hit_damage = monster.attack_player(player, multiplier=action.get("multiplier", 0.75))
                total_damage += hit_damage

            self.ui.trigger_player_hit_effect()
            self.ui.add_log(f"{monster.name} used {label} and dealt {total_damage} total damage.", LOG_COMBAT)
            self.ui.add_floating_text(f"-{total_damage}", 180, 210, color=(255, 90, 90))

            try_apply_status(monster, player, self.ui)

        else:
            enemy_damage = monster.attack_player(player, multiplier=action.get("multiplier", 1.0))
            self.ui.trigger_player_hit_effect()
            self.ui.add_log(f"{monster.name} used {label} and dealt {enemy_damage} damage to {player.name}.", LOG_COMBAT)
            self.ui.add_floating_text(f"-{enemy_damage}", 180, 210, color=(255, 90, 90))

            try_apply_status(monster, player, self.ui)

        if not player.player_is_alive():
            self.handle_player_defeat()
            return

        if not monster.enemy_is_alive():
            self.handle_monster_defeat()
            return

        self.battle.set_player_turn()
        self.battle.next_turn()

    def handle_monster_defeat(self):
        player = self.battle.player
        monster = self.battle.monster

        self.battle.set_victory()
        self.battle.monster = self.battle.rewards.handle_monster_defeat(player, monster)
        self.ui.sync_entities()
        self.ui.add_log(f"A new {self.battle.monster.name} appeared.", LOG_IMPORTANT)
        self.ui.show_battle_cry()
        self.battle.set_player_turn()

    def handle_player_defeat(self):
        self.battle.set_defeat()
        self.ui.open_revive_prompt()