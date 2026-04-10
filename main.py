import os

from battle.battle import BattleSystem
from player.save_manager import load_player, save_player
from ui.battle_screen import BattleScreen
from ui.character_creation_screen import CharacterCreationScreen


def main():
    if os.path.exists("save_data.json"):
        player = load_player()
    else:
        creation_screen = CharacterCreationScreen()
        player = creation_screen.run()
        save_player(player)

    battle = BattleSystem(player)
    screen = BattleScreen(battle)
    battle.bind_ui(screen)
    screen.run()


if __name__ == "__main__":
    main()