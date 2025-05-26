from battle import Battle
from rules import chose_class

def main():
    player = chose_class()
    Battle(player)
    
if __name__ == "__main__":
        main()