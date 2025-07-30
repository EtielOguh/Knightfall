def get_knight_skills(player):
    return [
            {
                "name": "Power Slash",
                "mana_cost": 30,
                "description": "Corte poderoso que causa dano dobrado.",
                "execute": lambda enemy: power_slash(player, enemy),
                "required_level": 1
            },
            {
                "name": "Shield Bash",
                "mana_cost": 40,
                "description": "Bash com escudo que causa dano e reduz ataque.",
                "execute": lambda enemy: shield_bash(player, enemy),
                "required_level": 5
            }
        ]

def power_slash(player, enemy):
    damage = player.attack * 2
    enemy.damage_received(damage)
    print(f"{player.name} usou *Power Slash* e causou {damage} de dano!")

def shield_bash(player, enemy):
    damage = int(player.attack * 1.2)
    enemy.damage_received(damage)
    print(f"{player.name} usou *Shield Bash* e causou {damage} de dano!")
    print("O ataque do inimigo foi reduzido temporariamente. (efeito fictício)")