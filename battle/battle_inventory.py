class BattleInventory:
    @staticmethod
    def get_bag_items(player):
        items = list(player.bag)

        if player.healpotions > 0:
            items.append({
                "name": "Heal Potion",
                "quantity": player.healpotions,
                "kind": "heal_potion"
            })

        if player.manapotions > 0:
            items.append({
                "name": "Mana Potion",
                "quantity": player.manapotions,
                "kind": "mana_potion"
            })

        return items