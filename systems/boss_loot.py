def get_boss_drop(zone, player_class):
    
    drops = {
        1: {
            "Knight": "Reaper Sword",
            "Archer": "Reaper Bow",
            "Thief": "Reaper Dagger",
            "Mage": "Reaper Staff"
        },
        2: {
            "Knight": "Bone Armor",
            "Archer": "Bone Longbow",
            "Thief": "Bone Twinblades",
            "Mage": "Bone Catalyst"
        },
        3: {
            "Knight": "Shadow Plate",
            "Archer": "Shadow Bow",
            "Thief": "Shadow Fang",
            "Mage": "Shadow Orb"
        },
        4: {
            "Knight": "Demon Greatsword",
            "Archer": "Demon Recurve",
            "Thief": "Demon Claws",
            "Mage": "Demon Core"
        }
    }

    return drops[zone][player_class]