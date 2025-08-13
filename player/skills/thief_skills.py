def get_thief_skills(player):
    return[
        {
        "name": "Shadow Step",
        "mana_cost": 30,
        "description": "Flecha de fogo poderosa causando dano.",
        "execute": lambda enemy: shadow_step(player,enemy),
        "required_level": 1
        },
        {
        "name": "Backstab",
        "mana_cost": 30,
        "description": "Atira 5 flechas causando dano.",
        "execute": lambda enemy: backstab(player,enemy),
        "required_level": 1
        }
    ]

def shadow_step(player,enemy):
    damage = player.attack *2
    enemy.damage_received(damage)
    print(f"{player.name} Usou *Shadow Step* e causou {damage} de dano!")
    
def backstab(player,enemy):
    damage = int(player.atack * 1.2)
    enemy.damage_received(damage)
    print(f"{player.name} usou *Backstab* e causou {damage} de dano")
    