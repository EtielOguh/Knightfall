from battle import Battle
from rules import load_or_create_player
from player.player_base import Player

def main():
    player = load_or_create_player()
    Battle(player)
    
if __name__ == "__main__":
        main()