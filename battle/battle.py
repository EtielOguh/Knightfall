from rules import spawn_monster, try_drop_item, try_drop_stone

from battle.battle_rewards import BattleRewards
from battle.battle_actions import BattleActions


class BattleSystem:
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    VICTORY = "victory"
    DEFEAT = "defeat"

    def __init__(self, player, ui=None):
        self.player = player
        self.monster = spawn_monster(player.zone, player)
        self.ui = ui

        self.rewards = BattleRewards(
            ui=self.ui,
            spawn_monster_func=spawn_monster,
            try_drop_stone_func=try_drop_stone,
            try_drop_item_func=try_drop_item
        )

        self.actions = None
        self.turn_state = self.PLAYER_TURN
        self.turn_count = 1

        self.pending_enemy_action = False
        self.enemy_action_delay = 250
        self.enemy_action_time = 0

    def bind_ui(self, ui):
        self.ui = ui
        self.rewards.ui = ui
        self.actions = BattleActions(self, ui)

    def is_player_turn(self):
        return self.turn_state == self.PLAYER_TURN

    def is_enemy_turn(self):
        return self.turn_state == self.ENEMY_TURN

    def is_defeat(self):
        return self.turn_state == self.DEFEAT

    def is_victory(self):
        return self.turn_state == self.VICTORY

    def set_player_turn(self):
        self.turn_state = self.PLAYER_TURN

    def set_enemy_turn(self):
        self.turn_state = self.ENEMY_TURN

    def set_defeat(self):
        self.turn_state = self.DEFEAT
        self.clear_enemy_turn_schedule()

    def set_victory(self):
        self.turn_state = self.VICTORY
        self.clear_enemy_turn_schedule()

    def next_turn(self):
        self.turn_count += 1

    def schedule_enemy_turn(self, current_time):
        self.turn_state = self.ENEMY_TURN
        self.pending_enemy_action = True
        self.enemy_action_time = current_time + self.enemy_action_delay

    def can_execute_enemy_turn(self, current_time):
        return (
            self.turn_state == self.ENEMY_TURN
            and self.pending_enemy_action
            and current_time >= self.enemy_action_time
        )

    def clear_enemy_turn_schedule(self):
        self.pending_enemy_action = False
        self.enemy_action_time = 0

    def run_from_battle(self):
        self.monster = spawn_monster(self.player.zone, self.player)
        self.turn_state = self.PLAYER_TURN
        self.clear_enemy_turn_schedule()