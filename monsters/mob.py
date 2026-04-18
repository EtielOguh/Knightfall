from random import randint, random


class Enemy:
    def __init__(self, name, level, attack, health, max_health, allowed_rarities,
                 ai_profile="aggressive", is_boss=False):
        self.name = name
        self.level = level
        self.attack = attack
        self.health = health
        self.max_health = max_health
        self.exp = 10 * level
        self.allowed_rarities = allowed_rarities

        self.ai_profile = ai_profile
        self.is_boss = is_boss

        self.guard_active = False
        self.turn_counter = 0

        self.status_effects = []
        self.status_chances = {}

    def enemy_is_alive(self):
        return self.health > 0

    def damage_received(self, damage):
        if self.guard_active:
            damage = max(0, int(damage * 0.6))
            self.guard_active = False

        self.health -= damage

    def attack_player(self, player, multiplier=1.0):
        damage = randint(self.attack - 1, self.attack + 5)
        damage = int(damage * multiplier)
        damage = max(0, damage - player.defense)

        if damage > player.health:
            damage = player.health

        player.health -= damage
        return damage

    def drop_money(self, player):
        money = self.level * 10
        player.money += money

    def hp_ratio(self):
        if self.max_health <= 0:
            return 0
        return self.health / self.max_health

    def apply_status_effect(self, effect):
        effect_type = effect.get("type")

        for existing in self.status_effects:
            if existing["type"] == effect_type:
                existing["duration"] = max(existing["duration"], effect["duration"])
                existing["value"] = max(existing["value"], effect["value"])
                return False

        self.status_effects.append(effect.copy())
        return True

    def decide_action(self, player):
        self.turn_counter += 1

        if self.ai_profile == "aggressive":
            return self._decide_aggressive(player)

        elif self.ai_profile == "cautious":
            return self._decide_cautious(player)

        elif self.ai_profile == "berserker":
            return self._decide_berserker(player)

        elif self.ai_profile == "trickster":
            return self._decide_trickster(player)

        return {"type": "attack", "multiplier": 1.0, "label": "Attack"}

    def _decide_aggressive(self, player):
        if random() < 0.20:
            return {"type": "attack", "multiplier": 1.25, "label": "Heavy Strike"}
        return {"type": "attack", "multiplier": 1.0, "label": "Attack"}

    def _decide_cautious(self, player):
        if self.hp_ratio() <= 0.35 and random() < 0.45:
            return {"type": "guard", "label": "Guard"}

        if random() < 0.15:
            return {"type": "attack", "multiplier": 1.15, "label": "Measured Strike"}

        return {"type": "attack", "multiplier": 1.0, "label": "Attack"}

    def _decide_berserker(self, player):
        if self.hp_ratio() <= 0.40:
            return {"type": "attack", "multiplier": 1.45, "label": "Rage Smash"}

        if random() < 0.25:
            return {"type": "attack", "multiplier": 1.20, "label": "Wild Blow"}

        return {"type": "attack", "multiplier": 1.0, "label": "Attack"}

    def _decide_trickster(self, player):
        roll = random()

        if roll < 0.18:
            return {"type": "double_attack", "multiplier": 0.75, "label": "Double Slash"}

        if roll < 0.35:
            return {"type": "attack", "multiplier": 1.30, "label": "Sneak Hit"}

        return {"type": "attack", "multiplier": 1.0, "label": "Attack"}