from battle.battle import BattleSystem
from player.save_manager import load_or_create_player

def main():
    player = load_or_create_player()
    battle = BattleSystem(player)
    battle.start()
    
if __name__ == "__main__":
        main()

#Teste para push 