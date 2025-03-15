import sys
import time

def battle_animation():
    for _ in range(3):
        for dots in ["", ".", "..", "..."]:
            sys.stdout.write(f"\rBattling{dots}   ")
            sys.stdout.flush()
            time.sleep(0.5)
    print("\rBattling... Complete!")