import time


class CombatUI:
    def __init__(self, char_delay=0.015, event_delay=0.6):
        self.char_delay = char_delay
        self.event_delay = event_delay

    def slow_print(self, text, delay=None):
        delay = self.char_delay if delay is None else delay
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()

    def event(self, text, pause=None):
        self.slow_print(text)
        time.sleep(self.event_delay if pause is None else pause)

    def show_status(self, player, monster):
        print("=" * 40)
        print(f"{player.name} Lv.{player.level}")
        print(f"HP {player.health}/{player.max_health} | MP {player.mana}/{player.mana_max}")
        print("-" * 40)
        print(f"{monster.name} Lv.{monster.level}")
        print(f"HP {monster.health}/{monster.max_health}")
        print("=" * 40)

    def show_turn_menu(self):
        print("\n[A] Attack  [P] Potion  [F] Run  [S] Skill")
        return input("> ").lower()

    def show_main_battle_menu(self):
        print("\n[A] Auto Attack  [B] Turn Battle  [P] Potion  [F] Run  [M] Menu")
        return input("Choose your action: ").lower()

    def show_full_menu(self):
        print("\n=== Full Menu ===")
        print("Z) Next Zone (-$50)")
        print("X) Back Zone (-$50)")
        print("I) Equip Items")
        print("S) Save and Exit")
        print("E) Show Bag")
        print("P) Boss Fight")
        print("D) Enable Dynamic Zone")
        print("H) Disable Dynamic Zone")
        print("M) Merchant")
        print("Q) Back to Battle\n")
        return input("Choose your option: ").lower()

    def show_potion_menu(self, player):
        heal_text = f"{player.healpotions} left" if player.healpotions > 0 else "Unavailable"
        mana_text = f"{player.manapotions} left" if player.manapotions > 0 else "Unavailable"

        print("\nWhich potion?")
        print(f"[1] Heal Potion - {heal_text}")
        print(f"[2] Mana Potion - {mana_text}")
        return input("Choice: ")