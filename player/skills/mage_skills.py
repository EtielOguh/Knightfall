def get_mage_skills(player):
    return[
        {
        "name": "Fire Ball",
        "mana_cost": 30,
        "description": "Flecha de fogo poderosa causando dano.",
        "execute": lambda enemy: fire_ball(player,enemy),
        "required_level": 1
        },
        {
        "name": "Icestorm",
        "mana_cost": 30,
        "description": "Atira 5 flechas causando dano.",
        "execute": lambda enemy: icestorm(player,enemy),
        "required_level": 1
        }
    ]

def fire_ball(player,enemy):
    damage = player.attack *2
    enemy.damage_received(damage)
    print(f"{player.name} Usou *Fire Ball* e causou {damage} de dano!")
    
def icestorm(player,enemy):
    damage = int(player.atack * 1.2)
    enemy.damage_received(damage)
    print(f"{player.name} usou *Icestorm* e causou {damage} de dano")
    