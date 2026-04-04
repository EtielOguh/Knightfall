import sys
import time

import sys
import time


def battle_animation():
    frames = [
        "o      o",
        "o>     o",
        "o->    o",
        "o-->   o",
        "o--->  o",
        "o----> o",
        "o----->o",
        "o----->x",
    ]

    for frame in frames:
        sys.stdout.write("\r" + frame + "   ")
        sys.stdout.flush()
        time.sleep(0.2)