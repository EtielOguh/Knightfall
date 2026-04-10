from rules import spawn_monster, try_drop_item, try_drop_stone
from battle.combat_ui import CombatUI
from battle.battle_rewards import BattleRewards
from battle.battle_actions import BattleActions


class BattleSystem:
    def __init__(self, player, ui=None):
        self.player = player
        self.monster = spawn_monster(player.zone, player)
        self.ui = ui or CombatUI()

        self.rewards = BattleRewards(
            ui=self.ui,
            spawn_monster_func=spawn_monster,
            try_drop_stone_func=try_drop_stone,
            try_drop_item_func=try_drop_item
        )

        self.actions = None

    def bind_ui(self, ui):
        self.ui = ui
        self.rewards.ui = ui
        self.actions = BattleActions(self, ui)

    def run_from_battle(self):
        self.monster = spawn_monster(self.player.zone, self.player)