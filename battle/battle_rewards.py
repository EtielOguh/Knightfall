from player.save_manager import save_player


class BattleRewards:
    def __init__(self, ui, spawn_monster_func, try_drop_stone_func, try_drop_item_func):
        self.ui = ui
        self.spawn_monster = spawn_monster_func
        self.try_drop_stone = try_drop_stone_func
        self.try_drop_item = try_drop_item_func

    def handle_monster_defeat(self, player, monster):
        self.ui.event(f"{monster.name} defeated!", 0.8)

        player.exp_wins(monster)
        self.ui.event("Experience gained.", 0.5)

        monster.drop_money(player)
        self.ui.event("Gold collected.", 0.5)

        player.potion_drops()
        self.try_drop_stone(monster, player)
        self.try_drop_item(player, monster)
        self.ui.event("Drops processed.", 0.6)

        save_player(player)
        self.ui.event("Progress saved.", 0.4)

        return self.spawn_monster(player.zone, player)