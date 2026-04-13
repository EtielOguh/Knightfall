from player.save_manager import save_player
from time import sleep


class BattleRewards:
    def __init__(self, ui, spawn_monster_func, try_drop_stone_func, try_drop_item_func):
        self.ui = ui
        self.spawn_monster = spawn_monster_func
        self.try_drop_stone = try_drop_stone_func
        self.try_drop_item = try_drop_item_func

    def handle_monster_defeat(self, player, monster):
        self.ui.event(f"{monster.name} defeated!", 0.5)

        player.exp_wins(monster)
        self.ui.event(f"+{monster.exp} EXP", 0.3)
        self.ui.event(f"XP: {player.xp}/{player.xp_max}", 0.3)

        monster.drop_money(player)
        self.ui.event("Gold collected.", 0.4)

        potion_drops = player.potion_drops()
        stone_drop = self.try_drop_stone(monster, player)
        item_drop = self.try_drop_item(player, monster)

        drops = []

        if potion_drops:
            drops.extend(potion_drops)

        if stone_drop:
            drops.append(stone_drop.name)

        if item_drop:
            drops.append(f"{item_drop.name} [{item_drop.rarity.name}]")

        if drops:
            self.ui.event(f"You got: {', '.join(drops)}", 0.4)
        else:
            self.ui.event("No drops.", 0.4)

        save_player(player)
        self.ui.event("Progress saved.", 0.4)
        return self.spawn_monster(player.zone, player)
        