import sys
import time

def battle_animation():
    swords = ["", "🗡", "🗡🗡", "🗡🗡🗡"]
    for _ in range(1):
        for swords_seq in swords:
            sys.stdout.write(f"\rBattling {swords_seq}   ")
            sys.stdout.flush()
            time.sleep(0.2)
    print("\rBattling 🗡🗡🗡 Complete!")