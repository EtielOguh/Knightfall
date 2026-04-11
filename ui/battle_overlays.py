import pygame

class BattleOverlays:
    @staticmethod
    def draw_menu_overlay(ui):
        overlay = pygame.Rect(300, 160, 400, 300)
        pygame.draw.rect(ui.screen, (20, 20, 20), overlay)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2)

        title = ui.font.render("Menu", True, (255, 255, 255))
        ui.screen.blit(title, (460, 185))

        options = ui.get_menu_options()
        y = 250

        for index, option in enumerate(options):
            prefix = ">" if index == ui.state.menu_index else " "
            line = f"{prefix} {option}"
            color = (230, 210, 120) if index == ui.state.menu_index else (220, 220, 220)

            text = ui.font.render(line, True, color)
            ui.screen.blit(text, (380, y))
            y += 50

        footer = ui.small_font.render("[ENTER] Select   [ESC] Close", True, (180, 180, 180))
        ui.screen.blit(footer, (360, 420))

    @staticmethod
    def draw_potions_overlay(ui):
        overlay = pygame.Rect(180, 120, 640, 420)
        pygame.draw.rect(ui.screen, (20, 20, 20), overlay)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2)

        title = ui.font.render("Potions", True, (255, 255, 255))
        ui.screen.blit(title, (445, 140))

        items = ui.get_potion_items()

        if not items:
            text = ui.small_font.render("No potions available.", True, (220, 220, 220))
            ui.screen.blit(text, (240, 200))
        else:
            y = 200
            for index, item in enumerate(items):
                prefix = ">" if index == ui.state.potion_index else " "
                line = f"{prefix} {item['name']} x{item['quantity']}"
                text = ui.small_font.render(line, True, (220, 220, 220))
                ui.screen.blit(text, (240, y))
                y += 30

        footer = ui.small_font.render("[ENTER] Use   [ESC] Close", True, (180, 180, 180))
        ui.screen.blit(footer, (240, 500))

    @staticmethod
    def draw_inventory_overlay(ui):
        overlay = pygame.Rect(80, 80, 840, 520)
        pygame.draw.rect(ui.screen, (20, 20, 20), overlay, border_radius=10)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2, border_radius=10)

        title = ui.font.render("Inventory", True, (255, 255, 255))
        ui.screen.blit(title, (430, 95))

        categories = ui.get_inventory_categories()

        # categorias em boxes
        x = 105
        y = 140
        tab_width = 110
        tab_height = 34
        tab_gap = 10

        for index, category in enumerate(categories):
            is_selected = index == ui.state.inventory_category_index
            tab_rect = pygame.Rect(x, y, tab_width, tab_height)

            fill_color = (55, 55, 70) if is_selected else (30, 30, 30)
            border_color = (230, 210, 120) if is_selected else (110, 110, 110)
            text_color = (255, 245, 190) if is_selected else (190, 190, 190)

            pygame.draw.rect(ui.screen, fill_color, tab_rect, border_radius=6)
            pygame.draw.rect(ui.screen, border_color, tab_rect, 2, border_radius=6)

            text = ui.small_font.render(category.capitalize(), True, text_color)
            text_rect = text.get_rect(center=tab_rect.center)
            ui.screen.blit(text, text_rect)

            x += tab_width + tab_gap

        # áreas internas
        list_rect = pygame.Rect(110, 195, 380, 320)
        detail_rect = pygame.Rect(535, 195, 275, 220)

        pygame.draw.rect(ui.screen, (26, 26, 26), list_rect, border_radius=8)
        pygame.draw.rect(ui.screen, (80, 80, 80), list_rect, 1, border_radius=8)

        pygame.draw.rect(ui.screen, (26, 26, 26), detail_rect, border_radius=8)
        pygame.draw.rect(ui.screen, (80, 80, 80), detail_rect, 1, border_radius=8)

        items = ui.get_inventory_items_by_category()

        y = 210
        if not items:
            text = ui.small_font.render("No items in this category.", True, (220, 220, 220))
            ui.screen.blit(text, (125, y))
        else:
            for index, item in enumerate(items):
                is_selected = index == ui.state.inventory_item_index

                row_rect = pygame.Rect(120, y - 2, 360, 24)
                if is_selected:
                    pygame.draw.rect(ui.screen, (45, 45, 60), row_rect, border_radius=4)
                    pygame.draw.rect(ui.screen, (230, 210, 120), row_rect, 1, border_radius=4)

                prefix = ">" if is_selected else " "
                atk = getattr(item, "attack", 0)
                defense = getattr(item, "defense", 0)
                qty = getattr(item, "quantity", 1)

                line = f"{prefix} {item.name}  ATK:{atk}  DEF:{defense}  x{qty}"
                color = (255, 245, 190) if is_selected else (220, 220, 220)

                text = ui.small_font.render(line, True, color)
                ui.screen.blit(text, (128, y))
                y += 28

            selected_item = items[ui.state.inventory_item_index]
            detail_x = 555
            detail_y = 215

            detail_title = ui.small_font.render("Item Details", True, (230, 210, 120))
            ui.screen.blit(detail_title, (detail_x, detail_y))
            detail_y += 35

            details = [
                f"Name: {selected_item.name}",
                f"ATK: {getattr(selected_item, 'attack', 0)}",
                f"DEF: {getattr(selected_item, 'defense', 0)}",
                f"Rarity: {getattr(selected_item, 'rarity', 'N/A')}",
                f"Category: {getattr(selected_item, 'category', 'misc')}",
                f"Slot: {getattr(selected_item, 'slot', 'N/A')}",
            ]

            for line in details:
                text = ui.small_font.render(str(line), True, (220, 220, 220))
                ui.screen.blit(text, (detail_x, detail_y))
                detail_y += 28

        footer = ui.small_font.render(
            "[ENTER] Equip   [ESC] Close   [LEFT/RIGHT] Category",
            True,
            (180, 180, 180),
        )
        ui.screen.blit(footer, (120, 560))
        
    @staticmethod
    def draw_skill_overlay(ui):
        overlay = pygame.Rect(180, 120, 640, 420)
        pygame.draw.rect(ui.screen, (20, 20, 20), overlay)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2)

        title = ui.font.render("Skills", True, (255, 255, 255))
        ui.screen.blit(title, (455, 140))

        skills = ui.player.skills

        if not skills:
            text = ui.small_font.render("No skills available.", True, (220, 220, 220))
            ui.screen.blit(text, (240, 200))
        else:
            y = 200
            for index, skill in enumerate(skills):
                prefix = ">" if index == ui.state.skill_index else " "
                line = f"{prefix} {skill['name']} | MP: {skill['mana_cost']} | {skill['description']}"
                text = ui.small_font.render(line, True, (220, 220, 220))
                ui.screen.blit(text, (240, y))
                y += 28

        footer = ui.small_font.render("[ENTER] Use   [ESC] Close", True, (180, 180, 180))
        ui.screen.blit(footer, (240, 500))

    @staticmethod
    def draw_equipped_overlay(ui):
        overlay = pygame.Rect(220, 120, 560, 400)
        pygame.draw.rect(ui.screen, (20, 20, 20), overlay)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2)

        title = ui.font.render("Equipped Items", True, (255, 255, 255))
        ui.screen.blit(title, (370, 145))

        y = 220
        for slot_name, item in ui.get_equipped_items():
            item_name = item.name if item else "Empty"
            line = f"{slot_name}: {item_name}"
            text = ui.small_font.render(line, True, (220, 220, 220))
            ui.screen.blit(text, (270, y))
            y += 45

        footer = ui.small_font.render("[ESC] Close", True, (180, 180, 180))
        ui.screen.blit(footer, (450, 470))