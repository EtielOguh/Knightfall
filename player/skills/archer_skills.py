def get_archer_skills(player):
    return[
        {
        "name": "Fire Arrow",
        "mana_cost": 30,
        "description": "Fire arrow that deals double damage",
        "execute": lambda enemy: fire_arrow(player,enemy),
        "required_level": 1
        },
        {
        "name": "Multi Shot",
        "mana_cost": 30,
        "description": "Shotting five arrows in a row",
        "execute": lambda enemy: multi_shot(player,enemy),
        "required_level": 1
        }
    ]

def fire_arrow(player,enemy):
    damage = player.attack *2
    enemy.damage_received(damage)
    print(f"{player.name} used *Fire Arrow* and dealt {damage} damage!")
    
def multi_shot(player,enemy):
    damage = int(player.attack * 1.2)
    enemy.damage_received(damage)
    print(f"{player.name} used *Multi Shot* and dealt {damage} damage")
    