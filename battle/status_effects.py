from random import random

STATUS_LIBRARY = {
    "poison": {
        "duration": 3,
        "value": 4,
        "name": "Poison",
    },
    "bleed": {
        "duration": 2,
        "value": 6,
        "name": "Bleed",
    },
    "burn": {
        "duration": 3,
        "value": 5,
        "name": "Burn",
    },
}


def build_status_effect(status_type: str):
    config = STATUS_LIBRARY.get(status_type)
    if not config:
        return None

    return {
        "type": status_type,
        "duration": config["duration"],
        "value": config["value"],
        "name": config["name"],
    }


def try_apply_status(attacker, target, ui=None):
    status_chances = getattr(attacker, "status_chances", {})

    if not status_chances:
        return None

    for status_type, chance in status_chances.items():
        if random() <= chance:
            effect = build_status_effect(status_type)
            if not effect:
                continue

            applied = target.apply_status_effect(effect)

            if applied and ui:
                ui.add_log(
                    f"{target.name} is affected by {effect['name']}!",
                    "important"
                )

            return effect if applied else None

    return None


def process_status_effects(entity, ui=None):
    if not hasattr(entity, "status_effects") or not entity.status_effects:
        return {
            "damage_taken": 0,
            "triggered": [],
            "died": False,
        }

    remaining_effects = []
    total_damage = 0
    triggered = []

    for effect in entity.status_effects:
        effect_type = effect.get("type")
        value = effect.get("value", 0)
        duration = effect.get("duration", 0)
        effect_name = effect.get("name", effect_type.title())

        if effect_type in ("poison", "bleed", "burn"):
            damage = min(entity.health, value)
            entity.health -= damage
            total_damage += damage
            triggered.append({
                "type": effect_type,
                "name": effect_name,
                "damage": damage,
            })

            if ui and damage > 0:
                ui.add_log(
                    f"{entity.name} took {damage} damage from {effect_name}.",
                    "combat"
                )

        duration -= 1

        if duration > 0:
            effect["duration"] = duration
            remaining_effects.append(effect)
        else:
            if ui:
                ui.add_log(
                    f"{effect_name} expired on {entity.name}.",
                    "system"
                )

    entity.status_effects = remaining_effects

    return {
        "damage_taken": total_damage,
        "triggered": triggered,
        "died": entity.health <= 0,
    }