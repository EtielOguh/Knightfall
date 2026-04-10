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
        #self.ui.add_log(f"{player.name} dealt {damage} damage to {monster.name}.")

        if monster.enemy_is_alive():
            enemy_damage = monster.attack_player(player)
            #self.ui.add_log(f"{monster.name} dealt {enemy_damage} damage to {player.name}.")
        else:
            self.battle.monster = self.battle.rewards.handle_monster_defeat(player, monster)
            self.ui.sync_entities()
            #self.ui.add_log(f"A new {self.battle.monster.name} appeared.")

    def run(self):
        self.ui.add_log("You ran away.")
        self.battle.run_from_battle()
        self.ui.sync_entities()

    def use_bag_item(self, item):
        player = self.battle.player

        if isinstance(item, dict):
            if item["kind"] == "heal_potion":
                if player.healpotions > 0:
                    player.use_heal_potion()
                    self.ui.add_log("Heal Potion used.")
                else:
                    self.ui.add_log("No Heal Potion left.")
                return

            if item["kind"] == "mana_potion":
                if player.manapotions > 0:
                    player.use_mana_potion()
                    self.ui.add_log("Mana Potion used.")
                else:
                    self.ui.add_log("No Mana Potion left.")
                return

        self.ui.add_log(f"{item.name} cannot be used in battle.")

    def use_skill(self, skill_index):
        player = self.battle.player
        monster = self.battle.monster

        if not player.player_is_alive() or not monster.enemy_is_alive():
            return

        result = player.use_skill(skill_index, monster)

        if not result["success"]:
            if result["reason"] == "invalid_skill":
                self.ui.add_log("Invalid skill.")
            elif result["reason"] == "no_mana":
                self.ui.add_log("Not enough mana.")
            return

        skill = result["skill"]
        damage = result["damage"]

        self.ui.add_log(f"{player.name} used {skill['name']} for {damage} damage.")

        if monster.enemy_is_alive():
            enemy_damage = monster.attack_player(player)
            self.ui.add_log(f"{monster.name} dealt {enemy_damage} damage to {player.name}.")
        else:
            self.battle.monster = self.battle.rewards.handle_monster_defeat(player, monster)
            self.ui.sync_entities()
            self.ui.add_log(f"A new {self.battle.monster.name} appeared.")