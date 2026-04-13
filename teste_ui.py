from player.save_manager import load_or_create_player
from rules import spawn_monster
from ui.battle_screen import BattleScreen

player = load_or_create_player()
monster = spawn_monster(player.zone, player)

screen = BattleScreen(player, monster)
screen.run()