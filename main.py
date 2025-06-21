from battle import Battle
from player.save_manager import load_or_create_player

def main():
    player = load_or_create_player()
    Battle(player)
    
if __name__ == "__main__":
        main()