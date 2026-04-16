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

        list_rect = pygame.Rect(110, 195, 380, 320)
        detail_rect = pygame.Rect(520, 195, 300, 300)

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

            detail_x = 540
            detail_y = 210

            # nome do item
            name_text = ui.font.render(selected_item.name, True, (255, 245, 190))
            ui.screen.blit(name_text, (detail_x, detail_y))
            detail_y += 45

            # espaço para imagem
            image_box = pygame.Rect(detail_x, detail_y, 96, 96)
            pygame.draw.rect(ui.screen, (35, 35, 35), image_box, border_radius=8)
            pygame.draw.rect(ui.screen, (120, 120, 120), image_box, 2, border_radius=8)

            placeholder = ui.small_font.render("ITEM", True, (170, 170, 170))
            placeholder_rect = placeholder.get_rect(center=image_box.center)
            ui.screen.blit(placeholder, placeholder_rect)

            # bloco de stats ao lado da imagem
            stat_x = detail_x + 115
            stat_y = detail_y + 5

            rarity_text = BattleOverlays.format_enum_value(getattr(selected_item, "rarity", "N/A"))
            slot_text = BattleOverlays.format_slot_name(getattr(selected_item, "slot", None))

            details = [
                f"ATK: {getattr(selected_item, 'attack', 0)}",
                f"DEF: {getattr(selected_item, 'defense', 0)}",
                f"Rarity: {rarity_text}",
                f"Category: {getattr(selected_item, 'category', 'misc').capitalize()}",
                f"Slot: {slot_text}",
                f"Qty: {getattr(selected_item, 'quantity', 1)}",
            ]

            for line in details:
                text = ui.small_font.render(line, True, (220, 220, 220))
                ui.screen.blit(text, (stat_x, stat_y))
                stat_y += 24

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
        overlay = pygame.Rect(90, 55, 820, 540)
        pygame.draw.rect(ui.screen, (18, 18, 18), overlay, border_radius=14)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2, border_radius=14)

        title = ui.font.render("Equipped Items", True, (255, 255, 255))
        title_rect = title.get_rect(center=(overlay.centerx, overlay.y + 28))
        ui.screen.blit(title, title_rect)

        pygame.draw.line(
            ui.screen,
            (55, 55, 55),
            (overlay.x + 28, overlay.y + 56),
            (overlay.right - 28, overlay.y + 56),
            1
        )

        slot_order = ["Head", "Left Hand", "Body", "Right Hand", "Foot"]

        equipped_map = {
            "Head": ui.player.head[0] if ui.player.head else None,
            "Left Hand": ui.player.left_hand[0] if ui.player.left_hand else None,
            "Body": ui.player.body[0] if ui.player.body else None,
            "Right Hand": ui.player.right_hand[0] if ui.player.right_hand else None,
            "Foot": ui.player.foot[0] if hasattr(ui.player, "foot") and ui.player.foot else None,
        }

        selected_index = max(0, min(ui.state.equipped_index, len(slot_order) - 1))
        selected_slot = slot_order[selected_index]
        selected_item = equipped_map[selected_slot]

        # painel esquerdo principal
        left_panel = pygame.Rect(120, 110, 430, 365)
        pygame.draw.rect(ui.screen, (22, 22, 22), left_panel, border_radius=12)
        pygame.draw.rect(ui.screen, (55, 55, 55), left_panel, 1, border_radius=12)

        # slots mais compactos
        slot_rects = {
            "Head": pygame.Rect(288, 128, 96, 96),
            "Left Hand": pygame.Rect(180, 248, 96, 96),
            "Body": pygame.Rect(288, 248, 96, 96),
            "Right Hand": pygame.Rect(396, 248, 96, 96),
            "Foot": pygame.Rect(288, 368, 96, 96),
        }

        for index, slot_name in enumerate(slot_order):
            rect = slot_rects[slot_name]
            item = equipped_map[slot_name]
            is_selected = index == selected_index

            BattleOverlays.draw_item_slot(
                ui=ui,
                rect=rect,
                label=slot_name,
                item=item,
                is_selected=is_selected
            )

        # nome do selecionado logo abaixo do grid, sem exagero
        selected_name = selected_item.name if selected_item else selected_slot
        selected_name_surface = ui.font.render(
            ui.truncate_text(selected_name, 22),
            True,
            (255, 245, 190) if selected_item else (145, 145, 145)
        )
        selected_name_rect = selected_name_surface.get_rect(center=(left_panel.centerx, 500))
        ui.screen.blit(selected_name_surface, selected_name_rect)

        # resumo curto abaixo do bloco esquerdo
        total_attack = sum(getattr(item, "attack", 0) for item in equipped_map.values() if item)
        total_defense = sum(getattr(item, "defense", 0) for item in equipped_map.values() if item)

        summary_text = ui.small_font.render(
            f"ATK Bonus: {total_attack}   |   DEF Bonus: {total_defense}",
            True,
            (190, 190, 190),
        )
        summary_rect = summary_text.get_rect(center=(left_panel.centerx, 530))
        ui.screen.blit(summary_text, summary_rect)

        # painel direito único
        details_rect = pygame.Rect(585, 110, 265, 365)
        BattleOverlays.draw_equipped_details_panel(
            ui,
            details_rect,
            selected_slot,
            selected_item
        )

        pygame.draw.line(
            ui.screen,
            (55, 55, 55),
            (overlay.x + 28, overlay.bottom - 48),
            (overlay.right - 28, overlay.bottom - 48),
            1
        )

        footer = ui.small_font.render(
            "[ARROWS] Navigate   [ESC] Close",
            True,
            (165, 165, 165),
        )
        footer_rect = footer.get_rect(center=(overlay.centerx, overlay.bottom - 24))
        ui.screen.blit(footer, footer_rect)
        
    @staticmethod
    def format_enum_value(value):
        if value is None:
            return "N/A"

        text = str(value)

        if "." in text:
            text = text.split(".")[-1]

        return text.replace("_", " ").upper()


    @staticmethod
    def format_slot_name(slot):
        if not slot:
            return "N/A"

        slot_map = {
            "right_hand": "Right Hand",
            "left_hand": "Left Hand",
            "head": "Head",
            "body": "Body",
            "foot": "Foot",
            "feet": "Feet",
            "jewel": "Jewel",
        }

        return slot_map.get(slot, str(slot).replace("_", " ").title())
    
    @staticmethod
    def draw_item_slot(ui, rect, label, item, is_selected=False):
        fill_color = (34, 34, 40) if item else (24, 24, 24)

        if is_selected:
            glow_rect = pygame.Rect(rect.x - 3, rect.y - 3, rect.width + 6, rect.height + 6)
            pygame.draw.rect(ui.screen, (78, 64, 18), glow_rect, border_radius=14)
            border_color = (255, 225, 110)
            label_color = (255, 225, 110)
        else:
            border_color = (100, 100, 100) if item else (60, 60, 60)
            label_color = (145, 145, 145)

        # label pequena acima
        label_surface = ui.small_font.render(label, True, label_color)
        label_rect = label_surface.get_rect(center=(rect.centerx, rect.y - 12))
        ui.screen.blit(label_surface, label_rect)

        # slot
        pygame.draw.rect(ui.screen, fill_color, rect, border_radius=12)
        pygame.draw.rect(ui.screen, border_color, rect, 2, border_radius=12)

        # brilho superior sutil
        pygame.draw.line(
            ui.screen,
            (72, 72, 82) if item else (38, 38, 38),
            (rect.x + 10, rect.y + 8),
            (rect.right - 10, rect.y + 8),
            1
        )

        # sprite ou placeholder
        if item:
            sprite = ui.get_item_sprite(item, size=(52, 52))
            if sprite:
                sprite_rect = sprite.get_rect(center=rect.center)
                ui.screen.blit(sprite, sprite_rect)
            else:
                placeholder = ui.small_font.render("ITEM", True, (130, 130, 130))
                placeholder_rect = placeholder.get_rect(center=rect.center)
                ui.screen.blit(placeholder, placeholder_rect)
                
    @staticmethod
    def draw_zone_overlay(ui):
        overlay = pygame.Rect(255, 155, 490, 300)
        pygame.draw.rect(ui.screen, (20, 20, 20), overlay, border_radius=12)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2, border_radius=12)

        title = ui.font.render("Zone Travel", True, (255, 255, 255))
        title_rect = title.get_rect(center=(overlay.centerx, overlay.y + 28))
        ui.screen.blit(title, title_rect)

        zone_data = ui.get_zone_travel_options()

        current_text = ui.small_font.render(
            f"Current Zone: {zone_data['current_zone_id']} - {zone_data['current_zone_name']}",
            True,
            (220, 220, 220)
        )
        ui.screen.blit(current_text, (overlay.x + 30, overlay.y + 70))

        options = []

        if zone_data["previous_zone"] is not None:
            options.append(("previous", zone_data["previous_zone"]))

        if zone_data["next_zone"] is not None:
            options.append(("next", zone_data["next_zone"]))

        y = overlay.y + 120

        if not options:
            no_option = ui.small_font.render("No travel options available.", True, (170, 170, 170))
            ui.screen.blit(no_option, (overlay.x + 30, y))
        else:
            for index, (direction, zone_info) in enumerate(options):
                is_selected = index == ui.state.zone_menu_index

                row_rect = pygame.Rect(overlay.x + 25, y - 4, 440, 58)

                if is_selected:
                    pygame.draw.rect(ui.screen, (45, 45, 60), row_rect, border_radius=8)
                    pygame.draw.rect(ui.screen, (230, 210, 120), row_rect, 1, border_radius=8)

                direction_text = "Return" if direction == "previous" else "Advance"
                unlocked = zone_info["unlocked"]

                status_text = "Available" if unlocked else "Locked"
                status_color = (80, 220, 120) if unlocked else (220, 90, 90)

                line_1 = f"{direction_text}: Zone {zone_info['zone_id']} - {zone_info['zone_name']}"
                line_2 = f"Required Level: {zone_info['required_level']}   |   Status: {status_text}"

                text_color = (255, 245, 190) if is_selected else (220, 220, 220)

                surface_1 = ui.small_font.render(line_1, True, text_color)
                ui.screen.blit(surface_1, (overlay.x + 40, y + 4))

                surface_2_req = ui.small_font.render(
                    f"Required Level: {zone_info['required_level']}",
                    True,
                    (180, 180, 180)
                )
                ui.screen.blit(surface_2_req, (overlay.x + 40, y + 28))

                surface_2_status = ui.small_font.render(
                    f"Status: {status_text}",
                    True,
                    status_color
                )
                ui.screen.blit(surface_2_status, (overlay.x + 245, y + 28))

                y += 70

        footer = ui.small_font.render("[UP/DOWN] Select   [ENTER] Travel   [ESC] Close", True, (180, 180, 180))
        footer_rect = footer.get_rect(center=(overlay.centerx, overlay.bottom - 24))
        ui.screen.blit(footer, footer_rect)

    @staticmethod
    def draw_equipped_details_panel(ui, rect, slot_label, item):
        pygame.draw.rect(ui.screen, (22, 22, 22), rect, border_radius=12)
        pygame.draw.rect(ui.screen, (65, 65, 65), rect, 1, border_radius=12)

        pad_x = 18
        pad_y = 18

        # =========================
        # Header
        # =========================
        title_surface = ui.small_font.render("Selected Slot", True, (230, 210, 120))
        ui.screen.blit(title_surface, (rect.x + pad_x, rect.y + pad_y))

        slot_surface = ui.small_font.render(slot_label, True, (215, 215, 215))
        ui.screen.blit(slot_surface, (rect.x + pad_x, rect.y + pad_y + 26))

        # =========================
        # Media row
        # =========================
        media_top = rect.y + 72
        image_box = pygame.Rect(rect.x + pad_x, media_top, 88, 88)

        pygame.draw.rect(ui.screen, (30, 30, 30), image_box, border_radius=10)
        pygame.draw.rect(ui.screen, (100, 100, 100), image_box, 2, border_radius=10)

        name_area_x = image_box.right + 16
        name_area_width = rect.right - name_area_x - pad_x

        if not item:
            empty_surface = ui.font.render("Empty", True, (135, 135, 135))
            empty_rect = empty_surface.get_rect()
            empty_rect.midleft = (name_area_x, image_box.centery - 8)
            ui.screen.blit(empty_surface, empty_rect)

            hint_surface = ui.small_font.render("No item equipped", True, (105, 105, 105))
            hint_rect = hint_surface.get_rect()
            hint_rect.midleft = (name_area_x, image_box.centery + 20)
            ui.screen.blit(hint_surface, hint_rect)
            return

        sprite = ui.get_item_sprite(item, size=(54, 54))
        if sprite:
            sprite_rect = sprite.get_rect(center=image_box.center)
            ui.screen.blit(sprite, sprite_rect)
        else:
            placeholder = ui.small_font.render("ITEM", True, (130, 130, 130))
            placeholder_rect = placeholder.get_rect(center=image_box.center)
            ui.screen.blit(placeholder, placeholder_rect)

        # Nome do item alinhado ao centro da imagem
        item_name = ui.truncate_text(item.name, 18)
        name_surface = ui.font.render(item_name, True, (255, 245, 190))
        name_rect = name_surface.get_rect()
        name_rect.midleft = (name_area_x, image_box.centery)
        ui.screen.blit(name_surface, name_rect)

        # =========================
        # Stats block
        # =========================
        rarity_text = BattleOverlays.format_enum_value(getattr(item, "rarity", "N/A"))
        slot_name = BattleOverlays.format_slot_name(getattr(item, "slot", None))
        category_name = str(getattr(item, "category", "misc")).replace("_", " ").title()

        info_lines = [
            f"ATK: {getattr(item, 'attack', 0)}",
            f"DEF: {getattr(item, 'defense', 0)}",
            f"Rarity: {rarity_text}",
            f"Slot: {slot_name}",
            f"Category: {category_name}",
        ]

        info_y = image_box.bottom + 26
        line_gap = 28

        for line in info_lines:
            surface = ui.small_font.render(line, True, (220, 220, 220))
            ui.screen.blit(surface, (rect.x + pad_x, info_y))
            info_y += line_gap

    @staticmethod
    def draw_revive_overlay(ui):
        overlay = pygame.Rect(220, 170, 560, 260)
        pygame.draw.rect(ui.screen, (18, 18, 18), overlay, border_radius=12)
        pygame.draw.rect(ui.screen, (200, 200, 200), overlay, 2, border_radius=12)

        title = ui.font.render("You Were Defeated", True, (220, 90, 90))
        title_rect = title.get_rect(center=(overlay.centerx, overlay.y + 35))
        ui.screen.blit(title, title_rect)

        preview = ui.state.revive_penalty_preview or {
            "xp_loss": 0,
            "loss_percent": 20,
            "will_level_down": False
        }

        line1 = ui.small_font.render(
            f"Revive with full HP/MP and spawn a new monster.",
            True,
            (220, 220, 220)
        )
        ui.screen.blit(line1, (overlay.x + 35, overlay.y + 85))

        line2 = ui.small_font.render(
            f"Penalty: lose {preview['xp_loss']} XP ({preview['loss_percent']}% of current XP bar).",
            True,
            (220, 220, 220)
        )
        ui.screen.blit(line2, (overlay.x + 35, overlay.y + 118))

        level_text = "This can reduce your level." if preview["will_level_down"] else "Your level will remain the same."
        level_color = (220, 100, 100) if preview["will_level_down"] else (180, 180, 180)
        line3 = ui.small_font.render(level_text, True, level_color)
        ui.screen.blit(line3, (overlay.x + 35, overlay.y + 151))

        footer = ui.small_font.render(
            "[ENTER] Revive   [ESC] Keep reading",
            True,
            (180, 180, 180)
        )
        footer_rect = footer.get_rect(center=(overlay.centerx, overlay.bottom - 28))
        ui.screen.blit(footer, footer_rect)