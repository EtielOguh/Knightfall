def get_mage_skills(player):
    return[
        {
        "name": "Fire Ball",
        "mana_cost": 30,
        "description": "Fire Ball that deals double damage",
        "execute": lambda enemy: fire_ball(player,enemy),
        "required_level": 1
        },
        {
        "name": "Icestorm",
        "mana_cost": 30,
        "description": "Casts an ice storm dealing damage to all enemies.",
        "execute": lambda enemy: icestorm(player,enemy),
        "required_level": 1
        }
    ]

def fire_ball(player,enemy):
    damage = player.attack *2
    enemy.damage_received(damage)
    print(f"{player.name} used *Fire Ball* and dealt {damage} damage!")
    
def icestorm(player,enemy):
    damage = int(player.attack * 1.2)
    enemy.damage_received(damage)
    print(f"{player.name} used *Icestorm* and dealt {damage} damage!")