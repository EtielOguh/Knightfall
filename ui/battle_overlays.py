import pygame

class BattleOverlays:
    @staticmethod
    def draw_menu_overlay(ui):
        options = ui.get_menu_options()

        # fundo escurecido
        dim = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 135))
        ui.screen.blit(dim, (0, 0))

        option_height = 46
        header_h = 70
        footer_h = 46
        body_padding = 18

        overlay_width = 420
        overlay_height = header_h + footer_h + (len(options) * option_height) + (body_padding * 2)

        overlay = pygame.Rect(
            (ui.width - overlay_width) // 2,
            (ui.height - overlay_height) // 2,
            overlay_width,
            overlay_height
        )

        pygame.draw.rect(ui.screen, (18, 18, 18), overlay, border_radius=14)
        pygame.draw.rect(ui.screen, (210, 210, 210), overlay, 2, border_radius=14)

        # título
        title = ui.font.render("Menu", True, (255, 255, 255))
        title_rect = title.get_rect(center=(overlay.centerx, overlay.y + 32))
        ui.screen.blit(title, title_rect)

        pygame.draw.line(
            ui.screen,
            (55, 55, 55),
            (overlay.x + 24, overlay.y + 58),
            (overlay.right - 24, overlay.y + 58),
            1
        )

        # opções
        start_y = overlay.y + 82
        for index, option in enumerate(options):
            is_selected = index == ui.state.menu_index

            row_rect = pygame.Rect(
                overlay.x + 26,
                start_y + index * option_height,
                overlay.width - 52,
                36
            )

            if is_selected:
                pygame.draw.rect(ui.screen, (48, 48, 62), row_rect, border_radius=8)
                pygame.draw.rect(ui.screen, (230, 210, 120), row_rect, 1, border_radius=8)

            prefix = "›" if is_selected else " "
            color = (255, 245, 190) if is_selected else (220, 220, 220)
            text = ui.font.render(f"{prefix} {option}", True, color)
            text_rect = text.get_rect(midleft=(row_rect.x + 14, row_rect.centery))
            ui.screen.blit(text, text_rect)

        # footer
        pygame.draw.line(
            ui.screen,
            (55, 55, 55),
            (overlay.x + 24, overlay.bottom - 42),
            (overlay.right - 24, overlay.bottom - 42),
            1
        )

        footer = ui.small_font.render(
            "[UP/DOWN] Navigate   [ENTER] Select   [ESC] Close",
            True,
            (175, 175, 175)
        )
        footer_rect = footer.get_rect(center=(overlay.centerx, overlay.bottom - 20))
        ui.screen.blit(footer, footer_rect)

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
        dim = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 150))
        ui.screen.blit(dim, (0, 0))

        overlay = pygame.Rect(48, 38, 904, 624)
        pygame.draw.rect(ui.screen, (12, 12, 14), overlay, border_radius=18)
        pygame.draw.rect(ui.screen, (170, 170, 170), overlay, 2, border_radius=18)

        # Header
        title = ui.menu_font.render("Bag", True, (245, 245, 245))
        title_rect = title.get_rect(center=(overlay.centerx, overlay.y + 32))
        ui.screen.blit(title, title_rect)

        pygame.draw.line(
            ui.screen,
            (40, 40, 40),
            (overlay.x + 26, overlay.y + 56),
            (overlay.right - 26, overlay.y + 56),
            1
        )

        categories = ui.get_inventory_categories()

        # Tabs
        tab_y = overlay.y + 60
        tab_x = overlay.x + 28
        tab_gap = 10
        available_width = overlay.width - 56
        tab_width = (available_width - tab_gap * (len(categories) - 1)) // len(categories)
        tab_height = 42

        for index, category in enumerate(categories):
            is_selected = index == ui.state.inventory_category_index
            rect = pygame.Rect(
                tab_x + index * (tab_width + tab_gap),
                tab_y,
                tab_width,
                tab_height
            )

            fill = (44, 44, 58) if is_selected else (22, 22, 24)
            border = (226, 205, 116) if is_selected else (82, 82, 82)
            text_color = (255, 244, 200) if is_selected else (180, 180, 180)

            pygame.draw.rect(ui.screen, fill, rect, border_radius=10)
            pygame.draw.rect(ui.screen, border, rect, 2, border_radius=10)

            label = category.replace("_", " ").title()
            surface = ui.small_font.render(label, True, text_color)
            ui.screen.blit(surface, surface.get_rect(center=rect.center))

        # Panels
        list_rect = pygame.Rect(76, 146, 448, 420)
        detail_rect = pygame.Rect(550, 146, 326, 420)

        pygame.draw.rect(ui.screen, (16, 16, 18), list_rect, border_radius=16)
        pygame.draw.rect(ui.screen, (58, 58, 58), list_rect, 1, border_radius=16)

        pygame.draw.rect(ui.screen, (16, 16, 18), detail_rect, border_radius=16)
        pygame.draw.rect(ui.screen, (58, 58, 58), detail_rect, 1, border_radius=16)

        # Titles
        items_title = ui.font.render("Items", True, (230, 210, 120))
        ui.screen.blit(items_title, (list_rect.x + 20, list_rect.y + 16))

        details_title = ui.font.render("Details", True, (230, 210, 120))
        ui.screen.blit(details_title, (detail_rect.x + 20, detail_rect.y + 16))

        items = ui.get_inventory_items_by_category()
        selected_index = max(0, min(ui.state.inventory_item_index, max(0, len(items) - 1)))

        # LISTA COM SCROLL VISUAL
        top_y = list_rect.y + 62
        row_height = 46
        visible_rows = 7

        start_index = 0
        if selected_index >= visible_rows:
            start_index = selected_index - visible_rows + 1

        visible_items = items[start_index:start_index + visible_rows]

        if not items:
            empty_text = ui.small_font.render("No items in this category.", True, (145, 145, 145))
            ui.screen.blit(empty_text, (list_rect.x + 20, list_rect.y + 76))
        else:
            for local_idx, item in enumerate(visible_items):
                real_idx = start_index + local_idx
                is_selected = real_idx == selected_index

                row_rect = pygame.Rect(
                    list_rect.x + 14,
                    top_y + local_idx * row_height,
                    list_rect.width - 34,
                    36
                )

                if is_selected:
                    pygame.draw.rect(ui.screen, (46, 46, 60), row_rect, border_radius=8)
                    pygame.draw.rect(ui.screen, (226, 205, 116), row_rect, 1, border_radius=8)

                name = ui.truncate_text(getattr(item, "name", "Unknown"), 20)
                atk = getattr(item, "attack", 0)
                defense = getattr(item, "defense", 0)
                qty = getattr(item, "quantity", 1)

                color = (255, 245, 190) if is_selected else (222, 222, 222)

                name_surface = ui.small_font.render(name, True, color)
                atk_surface = ui.small_font.render(f"ATK {atk}", True, color)
                def_surface = ui.small_font.render(f"DEF {defense}", True, color)
                qty_surface = ui.small_font.render(f"x{qty}", True, color)

                ui.screen.blit(name_surface, (row_rect.x + 12, row_rect.y + 8))
                ui.screen.blit(atk_surface, (row_rect.x + 185, row_rect.y + 8))
                ui.screen.blit(def_surface, (row_rect.x + 270, row_rect.y + 8))
                ui.screen.blit(qty_surface, (row_rect.right - 42, row_rect.y + 8))

            if len(items) > visible_rows:
                track = pygame.Rect(list_rect.right - 12, top_y, 4, visible_rows * row_height - 10)
                pygame.draw.rect(ui.screen, (42, 42, 42), track, border_radius=4)

                thumb_height = max(28, int(track.height * (visible_rows / len(items))))
                max_start = max(1, len(items) - visible_rows)
                thumb_y = track.y + int((start_index / max_start) * (track.height - thumb_height))
                thumb = pygame.Rect(track.x, thumb_y, track.width, thumb_height)
                pygame.draw.rect(ui.screen, (226, 205, 116), thumb, border_radius=4)

        # PAINEL DIREITO
        if items:
            selected_item = items[selected_index]

            name_surface = ui.font.render(
                ui.truncate_text(selected_item.name, 20),
                True,
                (255, 245, 190)
            )
            ui.screen.blit(name_surface, (detail_rect.x + 20, detail_rect.y + 60))

            image_box = pygame.Rect(detail_rect.x + 20, detail_rect.y + 110, 110, 110)
            pygame.draw.rect(ui.screen, (28, 28, 32), image_box, border_radius=12)
            pygame.draw.rect(ui.screen, (105, 105, 105), image_box, 2, border_radius=12)

            sprite = ui.get_item_sprite(selected_item, size=(64, 64))
            if sprite:
                sprite_rect = sprite.get_rect(center=image_box.center)
                ui.screen.blit(sprite, sprite_rect)
            else:
                placeholder = ui.small_font.render("ITEM", True, (140, 140, 140))
                ui.screen.blit(placeholder, placeholder.get_rect(center=image_box.center))

            stat_x = detail_rect.x + 150
            stat_y = detail_rect.y + 120

            rarity_text = BattleOverlays.format_enum_value(getattr(selected_item, "rarity", "N/A"))
            slot_text = BattleOverlays.format_slot_name(getattr(selected_item, "slot", None))
            category_text = str(getattr(selected_item, "category", "misc")).replace("_", " ").title()

            lines = [
                f"ATK: {getattr(selected_item, 'attack', 0)}",
                f"DEF: {getattr(selected_item, 'defense', 0)}",
                f"Rarity: {rarity_text}",
                f"Category: {category_text}",
                f"Slot: {slot_text}",
                f"Qty: {getattr(selected_item, 'quantity', 1)}",
            ]

            for line in lines:
                line_surface = ui.small_font.render(line, True, (225, 225, 225))
                ui.screen.blit(line_surface, (stat_x, stat_y))
                stat_y += 30

            # bloco inferior visual
            info_rect = pygame.Rect(detail_rect.x + 20, detail_rect.y + 250, detail_rect.width - 40, 124)
            pygame.draw.rect(ui.screen, (22, 22, 24), info_rect, border_radius=12)
            pygame.draw.rect(ui.screen, (50, 50, 50), info_rect, 1, border_radius=12)

            equipped_same_slot = None
            slot_name = getattr(selected_item, "slot", None)
            if slot_name == "right_hand" and ui.player.right_hand:
                equipped_same_slot = ui.player.right_hand[0]
            elif slot_name == "left_hand" and ui.player.left_hand:
                equipped_same_slot = ui.player.left_hand[0]
            elif slot_name == "head" and ui.player.head:
                equipped_same_slot = ui.player.head[0]
            elif slot_name == "body" and ui.player.body:
                equipped_same_slot = ui.player.body[0]
            elif slot_name == "foot" and ui.player.foot:
                equipped_same_slot = ui.player.foot[0]

            compare_title = ui.small_font.render("Slot Preview", True, (230, 210, 120))
            ui.screen.blit(compare_title, (info_rect.x + 14, info_rect.y + 12))

            if equipped_same_slot:
                equipped_name = ui.truncate_text(equipped_same_slot.name, 22)
                equipped_line = ui.small_font.render(
                    f"Current: {equipped_name}",
                    True,
                    (200, 200, 200)
                )
                ui.screen.blit(equipped_line, (info_rect.x + 14, info_rect.y + 42))

                compare_line = ui.small_font.render(
                    f"ATK {getattr(equipped_same_slot, 'attack', 0)} -> {getattr(selected_item, 'attack', 0)}"
                    f"   DEF {getattr(equipped_same_slot, 'defense', 0)} -> {getattr(selected_item, 'defense', 0)}",
                    True,
                    (220, 220, 220)
                )
                ui.screen.blit(compare_line, (info_rect.x + 14, info_rect.y + 72))
            else:
                empty_slot_line = ui.small_font.render(
                    "Current: Empty slot",
                    True,
                    (200, 200, 200)
                )
                ui.screen.blit(empty_slot_line, (info_rect.x + 14, info_rect.y + 42))

                compare_line = ui.small_font.render(
                    f"New item will be equipped directly.",
                    True,
                    (220, 220, 220)
                )
                ui.screen.blit(compare_line, (info_rect.x + 14, info_rect.y + 72))

        # Footer
        pygame.draw.line(
            ui.screen,
            (40, 40, 40),
            (overlay.x + 26, overlay.bottom - 48),
            (overlay.right - 26, overlay.bottom - 48),
            1
        )

        footer = ui.small_font.render(
            "[LEFT/RIGHT] Category   [UP/DOWN] Select   [ENTER] Equip   [ESC] Close",
            True,
            (170, 170, 170)
        )
        footer_rect = footer.get_rect(center=(overlay.centerx, overlay.bottom - 24))
        ui.screen.blit(footer, footer_rect)

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