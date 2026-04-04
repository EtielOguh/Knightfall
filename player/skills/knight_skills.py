def get_knight_skills(player):
    return [
            {
                "name": "Power Slash",
                "mana_cost": 30,
                "description": "A powerfull slash givin double damage.",
                "execute": lambda enemy: power_slash(player, enemy),
                "required_level": 1
            },
            {
                "name": "Shield Bash",
                "mana_cost": 40,
                "description": "Bash your shield giving damage",
                "execute": lambda enemy: shield_bash(player, enemy),
                "required_level": 5
            }
        ]

def power_slash(player, enemy):
    damage = player.attack * 2
    enemy.damage_received(damage)
    print(f"{player.name} used *Power Slash* and give {damage} damage!")

def shield_bash(player, enemy):
    damage = int(player.attack * 1.2)
    enemy.damage_received(damage)
    enemy.attack - 2
    print(f"{player.name} used *Shield Bash* and give {damage} damage!")
