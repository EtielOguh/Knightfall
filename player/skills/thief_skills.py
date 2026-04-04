def get_thief_skills(player):
    return[
        {
        "name": "Shadow Step",
        "mana_cost": 30,
        "description": "Moves behind the enemy and strikes.",
        "execute": lambda enemy: shadow_step(player,enemy),
        "required_level": 1
        },
        {
        "name": "Backstab",
        "mana_cost": 30,
        "description": "Stabs the enemy from behind.",
        "execute": lambda enemy: backstab(player,enemy),
        "required_level": 1
        }
    ]

def shadow_step(player,enemy):
    damage = player.attack *2
    enemy.damage_received(damage)
    print(f"{player.name} used *Shadow Step* and dealt {damage} damage!")
    
def backstab(player,enemy):
    damage = int(player.attack * 1.2)
    enemy.damage_received(damage)
    print(f"{player.name} used *Backstab* and dealt {damage} damage")
    