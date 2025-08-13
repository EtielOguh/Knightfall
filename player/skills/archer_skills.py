def get_archer_skills(player):
    return[
        {
        "name": "Fire Arrow",
        "mana_cost": 30,
        "description": "Flecha de fogo poderosa causando dano.",
        "execute": lambda enemy: fire_arrow(player,enemy),
        "required_level": 1
        },
        {
        "name": "Multi Shot",
        "mana_cost": 30,
        "description": "Atira 5 flechas causando dano.",
        "execute": lambda enemy: multi_shot(player,enemy),
        "required_level": 1
        }
    ]

def fire_arrow(player,enemy):
    damage = player.attack *2
    enemy.damage_received(damage)
    print(f"{player.name} Usou *Fire Arrow* e causou {damage} de dano!")
    
def multi_shot(player,enemy):
    damage = int(player.atack * 1.2)
    enemy.damage_received(damage)
    print(f"{player.name} usou *Multi Shot* e causou {damage} de dano")
    