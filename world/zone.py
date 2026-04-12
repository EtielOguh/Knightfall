ZONES = {
    1: {"name": "Green Fields", "min_level": 1},
    2: {"name": "Dark Forest", "min_level": 5},
    3: {"name": "Ancient Ruins", "min_level": 9},
    4: {"name": "Cursed Depths", "min_level": 13},
}


def get_zone_name(zone_id):
    zone = ZONES.get(zone_id)
    if not zone:
        return f"Zone {zone_id}"
    return zone["name"]


def get_zone_min_level(zone_id):
    zone = ZONES.get(zone_id)
    if not zone:
        return 999
    return zone["min_level"]


def get_next_zone_id(current_zone):
    next_zone = current_zone + 1
    if next_zone in ZONES:
        return next_zone
    return None


def can_access_zone(player, zone_id):
    if zone_id not in ZONES:
        return False

    required_level = get_zone_min_level(zone_id)
    return player.level >= required_level


def can_advance_zone(player):
    next_zone = get_next_zone_id(player.zone)

    if next_zone is None:
        return False, None, "You are already in the last zone."

    required_level = get_zone_min_level(next_zone)

    if player.level < required_level:
        return False, next_zone, f"Level {required_level} required."

    return True, next_zone, f"Zone {next_zone} unlocked."

def change_zone(player, new_zone):
    if new_zone not in ZONES:
        return False, "Invalid zone."

    # Se estiver voltando, permite sem restrição
    if new_zone < player.zone:
        player.zone = new_zone
        return True, f"You returned to {get_zone_name(new_zone)}."

    required_level = get_zone_min_level(new_zone)

    if player.level < required_level:
        return False, f"You need level {required_level} to enter {get_zone_name(new_zone)}."

    player.zone = new_zone
    return True, f"You entered {get_zone_name(new_zone)}."


def get_next_zone_preview(player):
    next_zone = get_next_zone_id(player.zone)

    if next_zone is None:
        return {
            "has_next": False,
            "message": "No more zones available."
        }

    required_level = get_zone_min_level(next_zone)
    unlocked = player.level >= required_level

    return {
        "has_next": True,
        "zone_id": next_zone,
        "zone_name": get_zone_name(next_zone),
        "required_level": required_level,
        "unlocked": unlocked,
    }
    
def get_previous_zone_id(current_zone):
    previous_zone = current_zone - 1
    if previous_zone in ZONES:
        return previous_zone
    return None

def get_zone_travel_options(player):
    previous_zone = get_previous_zone_id(player.zone)
    next_zone = get_next_zone_id(player.zone)

    data = {
        "current_zone_id": player.zone,
        "current_zone_name": get_zone_name(player.zone),
        "previous_zone": None,
        "next_zone": None,
    }

    if previous_zone is not None:
        data["previous_zone"] = {
            "zone_id": previous_zone,
            "zone_name": get_zone_name(previous_zone),
            "required_level": get_zone_min_level(previous_zone),
            "unlocked": True,  # voltar não precisa bloquear
        }

    if next_zone is not None:
        required_level = get_zone_min_level(next_zone)
        data["next_zone"] = {
            "zone_id": next_zone,
            "zone_name": get_zone_name(next_zone),
            "required_level": required_level,
            "unlocked": player.level >= required_level,
        }

    return data