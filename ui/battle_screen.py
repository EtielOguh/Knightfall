import os
import random
import pygame
from battle.log_types import LOG_COMBAT, LOG_SYSTEM, LOG_IMPORTANT
from world.zone import get_zone_name, get_zone_background, change_zone
from ui.battle_ui_state import BattleUIState
from ui.battle_overlays import BattleOverlays
from ui.battle_screen_queries import BattleScreenQueries
from player.save_manager import save_player


class BattleScreen:
    # =========================
    # Constantes visuais / UI
    # =========================
    INVENTORY_CATEGORIES = ["weapon", "shield", "armor", "helmet", "jewel", "misc"]
    MENU_OPTIONS = ["Bag", "Equipped", "Zone Travel", "Save and Exit", "Close"]

    ACTIONS = [
        ("[1]", "Attack"),
        ("[2]", "Skill"),
        ("[3]", "Potions"),
        ("[4]", "Run"),
        ("[5]", "Menu"),
    ]

    PLAYER_POS = (200, 230)
    ENEMY_POS = (640, 230)

    # =========================
    # Inicialização
    # =========================
    def __init__(self, battle, width=1000, height=700):
        pygame.init()

        self.battle = battle
        self.width = width
        self.height = height

        self.enemy_hit_timer = 0
        self.enemy_flash_timer = 0
        self.enemy_shake_intensity = 0

        self.pending_enemy_action = False
        self.enemy_acion_delay = 250
        self.enemy_action_time = 0
    

        self.player_hit_timer = 0
        self.player_flash_timer = 0
        self.player_shake_intensity = 0

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Knightfall")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16)
        self.menu_font = pygame.font.SysFont("arial", 28, bold=True)

        self.state = BattleUIState()
        self.floating_texts = []
        self.running = True

        # Carrega player/monster/sprites/background
        self.sync_entities()
        self.show_battle_cry()

    def get_time(self):
        return pygame.time.get_ticks()
    
    def update_pending_battle_actions(self):
        if self.battle.can_execute_enemy_turn(self.get_time()):
            self.battle.actions.enemy_take_turn()
    
    # =========================
    # Salvar e sair
    # =========================
    def save_and_exit(self):
        save_player(self.player)
        self.running = False

    # =========================
    # Sincronização de entidades
    # =========================
    def _sync_entities(self):
        """
        Mantém referências locais sincronizadas com o BattleSystem.
        Se você já tiver esse método em outro lugar, preserve a lógica real.
        """
        self.player = self.battle.player
        self.monster = self.battle.monster

    def sync_entities(self):
        """Atualiza referências e recursos visuais dependentes da batalha atual."""
        self._sync_entities()
        self.player_sprite = self._load_sprite("player", self._get_player_sprite_name())
        self.enemy_sprite = self._load_sprite("enemies", self.monster.name)
        self._load_background()

    # =========================
    # Carregamento de assets
    # =========================
    def _load_background(self):
        bg_path = get_zone_background(self.player.zone)

        if not os.path.exists(bg_path):
            bg_path = "assets/background/battle_bg.png"

        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def _normalize_name(self, name):
        return name.lower().replace(" ", "_")

    def _get_player_sprite_name(self):
        class_map = {
            1: "knight",
            2: "archer",
            3: "thief",
            4: "mage",
        }
        return class_map.get(self.player.class_type, "knight")

    def _load_sprite(self, folder, name, size=(250, 250)):
        filename = f"{self._normalize_name(name)}.png"
        path = os.path.join("assets", folder, filename)

        if not os.path.exists(path):
            return None

        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def get_item_sprite(self, item, size=(52, 52)):
        """Busca sprite do item pelo sprite_name ou name."""
        if item is None:
            return None

        possible_names = []

        item_sprite_name = getattr(item, "sprite_name", None)
        if item_sprite_name:
            possible_names.append(self._normalize_name(item_sprite_name))

        item_name = getattr(item, "name", None)
        if item_name:
            normalized_name = self._normalize_name(item_name)
            if normalized_name not in possible_names:
                possible_names.append(normalized_name)

        for name in possible_names:
            path = os.path.join("assets", "items", f"{name}.png")
            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(image, size)

        return None

    # =========================
    # Feedback de batalha
    # =========================
    
    def add_log(self, text, log_type=LOG_COMBAT):
        self.state.add_log(text, log_type)
        
    def event(self, text, delay=0):
        # Mantido por compatibilidade
        self.add_log(text)

    def show_battle_cry(self):
        if hasattr(self.monster, "battle_cry"):
            cry = self.monster.battle_cry()
            if cry:
                self.add_log(cry, LOG_COMBAT)

    def add_floating_text(self, text, x, y, color=(255, 80, 80), duration=45):
        self.floating_texts.append(
            {
                "text": str(text),
                "x": x,
                "y": y,
                "color": color,
                "duration": duration,
            }
        )

    def update_floating_texts(self):
        for entry in self.floating_texts:
            entry["y"] -= 1
            entry["duration"] -= 1

        self.floating_texts = [
            entry for entry in self.floating_texts
            if entry["duration"] > 0
        ]
        
    def update_hit_effects(self):
        if self.enemy_hit_timer > 0:
            self.enemy_hit_timer -= 1

        if self.enemy_flash_timer > 0:
            self.enemy_flash_timer -= 1

        if self.player_hit_timer > 0:
            self.player_hit_timer -= 1

        if self.player_flash_timer > 0:
            self.player_flash_timer -= 1
            
    def apply_damage_flash(self, sprite, intensity=120):
        if sprite is None:
            return None

        flashed = sprite.copy()
        w, h = sprite.get_size()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)

        center_x = w // 2
        center_y = h // 2
        radius = min(w, h) // 3

        # desenha círculo suave
        for r in range(radius, 0, -1):
            alpha = int(intensity * (r / radius))
            pygame.draw.circle(
                overlay,
                (255, 50, 50, alpha),
                (center_x, center_y),
                r
            )

        flashed.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return flashed

    # =========================
    # Queries / dados derivados
    # =========================
    def get_zone_travel_options(self):
        return BattleScreenQueries.get_zone_travel_options(self)

    def get_bag_items(self):
        return BattleScreenQueries.get_bag_items(self)

    def get_potion_items(self):
        return BattleScreenQueries.get_potion_items(self)

    def get_inventory_categories(self):
        return BattleScreenQueries.get_inventory_categories(self)

    def get_current_inventory_category(self):
        return BattleScreenQueries.get_current_inventory_category(self)

    def get_inventory_items_by_category(self):
        return BattleScreenQueries.get_inventory_items_by_category(self)

    def get_equipped_items(self):
        return BattleScreenQueries.get_equipped_items(self)

    def get_menu_options(self):
        return BattleScreenQueries.get_menu_options(self)

    def get_zone_preview(self):
        return BattleScreenQueries.get_zone_preview(self)

    def get_current_zone_name(self):
        return get_zone_name(self.player.zone)

    # =========================
    # Transição de zona
    # =========================
    def start_zone_transition(self, target_zone_id):
        self.state.zone_transition_active = True
        self.state.zone_transition_phase = "fade_out"
        self.state.zone_transition_alpha = 0
        self.state.pending_zone_id = target_zone_id
        self.state.zone_title_timer = 0
        self.state.zone_title_text = ""

    def update_zone_transition(self):
        if not self.state.zone_transition_active:
            return

        fade_speed = 18

        if self.state.zone_transition_phase == "fade_out":
            self.state.zone_transition_alpha += fade_speed

            if self.state.zone_transition_alpha >= 255:
                self.state.zone_transition_alpha = 255

                target_zone_id = self.state.pending_zone_id
                success, message = change_zone(self.player, target_zone_id)
                self.add_log(message, LOG_IMPORTANT)

                if success:
                    self.battle.run_from_battle()
                    self.sync_entities()
                    self.show_battle_cry()
                    
                self.state.zone_transition_phase = "fade_in"

        elif self.state.zone_transition_phase == "fade_in":
            self.state.zone_transition_alpha -= fade_speed

            if self.state.zone_transition_alpha <= 0:
                self.state.zone_transition_alpha = 0
                self.state.zone_transition_phase = None
                self.state.zone_transition_active = False
                self.state.pending_zone_id = None

        if self.state.zone_title_timer > 0:
            self.state.zone_title_timer -= 1

    def draw_zone_transition(self):
        if self.state.zone_transition_alpha > 0:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(self.state.zone_transition_alpha)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
    # =========================
    # Input principal
    # =========================

    def handle_equipped_input(self, event):
        slot_count = 5  # Head, Left Hand, Body, Right Hand, Foot

        if event.key == pygame.K_ESCAPE:
            self.state.show_equipped = False
            return

        if event.key == pygame.K_LEFT:
            self.state.equipped_index = max(0, self.state.equipped_index - 1)

        elif event.key == pygame.K_RIGHT:
            self.state.equipped_index = min(slot_count - 1, self.state.equipped_index + 1)

        elif event.key == pygame.K_UP:
            if self.state.equipped_index in [1, 2, 3, 4]:
                self.state.equipped_index = 0

        elif event.key == pygame.K_DOWN:
            if self.state.equipped_index == 0:
                self.state.equipped_index = 2
            elif self.state.equipped_index in [1, 2, 3]:
                self.state.equipped_index = 4
                
    def handle_input(self, event):

        if event.type != pygame.KEYDOWN:
            return

        if self.state.zone_transition_active:
            return

        if self.state.show_revive_prompt:
            self.handle_revive_input(event)
            return
        
        if event.type != pygame.KEYDOWN:
            return

        # Durante transição, bloqueia qualquer input
        if self.state.zone_transition_active:
            return

        if self.state.show_potions:
            self.handle_potion_input(event)
            return

        if self.state.show_zone_menu:
            self.handle_zone_input(event)
            return

        if self.state.show_menu:
            self.handle_menu_input(event)
            return

        if self.state.show_inventory:
            self.handle_inventory_input(event)
            return

        if self.state.show_equipped:
            self.handle_equipped_input(event)
            return

        if self.state.show_skills:
            self.handle_skill_input(event)
            return

        self.handle_root_input(event)

    def handle_root_input(self, event):
        if not self.battle.is_player_turn():
            return

        if event.key == pygame.K_1:
            self.battle.actions.attack()

        elif event.key == pygame.K_2:
            self.state.show_skills = True
            self.state.skill_index = 0

        elif event.key == pygame.K_3:
            self.state.show_potions = True
            self.state.potion_index = 0

        elif event.key == pygame.K_4:
            self.battle.actions.run()

        elif event.key == pygame.K_5:
            self.state.show_menu = True
            self.state.menu_index = 0

    # =========================
    # Inputs de overlays / menus
    # =========================
    def _execute_menu_option(self, selected):
        if selected == "Bag":
            self.state.show_menu = False
            self.state.show_inventory = True
            self.state.inventory_category_index = 0
            self.state.inventory_item_index = 0

        elif selected == "Equipped":
            self.state.show_menu = False
            self.state.show_equipped = True
            self.state.equipped_index = 0

        elif selected == "Zone Travel":
            self.state.show_menu = False
            self.state.show_zone_menu = True
            self.state.zone_menu_index = 0

        elif selected == "Save and Exit":
            self.state.show_menu = False
            self.save_and_exit()

        elif selected == "Close":
            self.state.show_menu = False

    def handle_menu_input(self, event):
        options = self.get_menu_options()

        if event.key == pygame.K_ESCAPE:
            self.state.show_menu = False
            return

        if event.key == pygame.K_UP:
            self.state.menu_index = max(0, self.state.menu_index - 1)

        elif event.key == pygame.K_DOWN:
            self.state.menu_index = min(len(options) - 1, self.state.menu_index + 1)

        elif event.key == pygame.K_RETURN:
            selected = options[self.state.menu_index]
            self._execute_menu_option(selected)

    def handle_zone_input(self, event):
        options = []
        zone_data = self.get_zone_travel_options()

        if zone_data["previous_zone"] is not None:
            options.append(("previous", zone_data["previous_zone"]))

        if zone_data["next_zone"] is not None:
            options.append(("next", zone_data["next_zone"]))

        if event.key == pygame.K_ESCAPE:
            self.state.show_zone_menu = False
            return

        if not options:
            if event.key == pygame.K_RETURN:
                self.state.show_zone_menu = False
            return

        if event.key == pygame.K_UP:
            self.state.zone_menu_index = max(0, self.state.zone_menu_index - 1)

        elif event.key == pygame.K_DOWN:
            self.state.zone_menu_index = min(len(options) - 1, self.state.zone_menu_index + 1)

        elif event.key == pygame.K_RETURN:
            _, selected_zone = options[self.state.zone_menu_index]
            self.start_zone_transition(selected_zone["zone_id"])
            self.state.show_zone_menu = False

    def handle_potion_input(self, event):
        items = self.get_potion_items()

        if event.key == pygame.K_ESCAPE:
            self.state.show_potions = False
            return

        if not items:
            if event.key == pygame.K_RETURN:
                self.state.show_potions = False
            return

        if event.key == pygame.K_UP:
            self.state.potion_index = max(0, self.state.potion_index - 1)

        elif event.key == pygame.K_DOWN:
            self.state.potion_index = min(len(items) - 1, self.state.potion_index + 1)

        elif event.key == pygame.K_RETURN:
            selected_item = items[self.state.potion_index]
            self.battle.actions.use_bag_item(selected_item)
            self.state.show_potions = False

    def handle_skill_input(self, event):
        skills = self.player.skills

        if event.key == pygame.K_ESCAPE:
            self.state.show_skills = False
            return

        if not skills:
            if event.key == pygame.K_RETURN:
                self.state.show_skills = False
            return

        if event.key == pygame.K_UP:
            self.state.skill_index = max(0, self.state.skill_index - 1)

        elif event.key == pygame.K_DOWN:
            self.state.skill_index = min(len(skills) - 1, self.state.skill_index + 1)

        elif event.key == pygame.K_RETURN:
            self.battle.actions.use_skill(self.state.skill_index)
            self.state.show_skills = False

    def handle_inventory_input(self, event):
        categories = self.get_inventory_categories()
        items = self.get_inventory_items_by_category()

        if event.key == pygame.K_ESCAPE:
            self.state.show_inventory = False
            return

        if event.key == pygame.K_LEFT:
            self.state.inventory_category_index = max(0, self.state.inventory_category_index - 1)
            self.state.inventory_item_index = 0
            return

        elif event.key == pygame.K_RIGHT:
            self.state.inventory_category_index = min(
                len(categories) - 1,
                self.state.inventory_category_index + 1,
            )
            self.state.inventory_item_index = 0
            return

        elif event.key == pygame.K_UP:
            self.state.inventory_item_index = max(0, self.state.inventory_item_index - 1)
            return

        elif event.key == pygame.K_DOWN:
            self.state.inventory_item_index = min(
                max(0, len(items) - 1),
                self.state.inventory_item_index + 1,
            )
            return

        elif event.key == pygame.K_RETURN and items:
            old_index = self.state.inventory_item_index
            selected_item = items[old_index]
            selected_name = getattr(selected_item, "name", None)
            selected_slot = getattr(selected_item, "slot", None)

            self.battle.actions.try_equip_item(selected_item)

            # recalcula a lista da categoria após equipar
            updated_items = self.get_inventory_items_by_category()

            if not updated_items:
                self.state.inventory_item_index = 0
                return

            # tenta manter foco em item semelhante que permaneceu na bag
            fallback_index = min(old_index, len(updated_items) - 1)
            new_index = fallback_index

            for i, item in enumerate(updated_items):
                if (
                    getattr(item, "name", None) == selected_name
                    and getattr(item, "slot", None) == selected_slot
                ):
                    new_index = i
                    break

            self.state.inventory_item_index = new_index

    # =========================
    # Helpers de texto / layout
    # =========================
    def truncate_text(self, text, max_len=12):
        if not text:
            return ""
        if len(text) <= max_len:
            return text
        return text[:max_len - 3] + "..."

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = word if not current_line else current_line + " " + word

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)

        if current_line:
            lines.append(current_line)

        return lines

    # =========================
    # Draw principal
    # =========================
    def draw(self):
        self.draw_background()
        self.draw_zone_label()
        self.draw_battle_area()
        self.draw_hud()
        self.draw_action_bar()
        self.draw_log_box()
        self.draw_floating_texts()
        self.draw_active_overlay()
        self.draw_zone_transition()
        pygame.display.flip()

    def draw_active_overlay(self):
        if self.state.show_revive_prompt:
            BattleOverlays.draw_revive_overlay(self)
        elif self.state.show_zone_menu:
            BattleOverlays.draw_zone_overlay(self)
        elif self.state.show_potions:
            BattleOverlays.draw_potions_overlay(self)
        elif self.state.show_menu:
            BattleOverlays.draw_menu_overlay(self)
        elif self.state.show_inventory:
            BattleOverlays.draw_inventory_overlay(self)
        elif self.state.show_equipped:
            BattleOverlays.draw_equipped_overlay(self)
        elif self.state.show_skills:
            BattleOverlays.draw_skill_overlay(self)

    def draw_background(self):
        if hasattr(self, "background") and self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((10, 10, 10))

    def draw_zone_label(self):
        zone_name = self.get_current_zone_name()
        label_rect = pygame.Rect(370, 16, 260, 36)

        pygame.draw.rect(self.screen, (14, 14, 14), label_rect, border_radius=12)
        pygame.draw.rect(self.screen, (80, 80, 80), label_rect, 1, border_radius=12)

        text_surface = self.small_font.render(
            f"Zone {self.player.zone} - {zone_name}",
            True,
            (230, 210, 120),
        )
        text_rect = text_surface.get_rect(center=label_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_battle_area(self):
        player_pos = list(self.PLAYER_POS)
        enemy_pos = list(self.ENEMY_POS)

        # shake do player
        if self.player_hit_timer > 0:
            offset_x = random.randint(-self.player_shake_intensity, self.player_shake_intensity)
            offset_y = random.randint(-2, 2)
            player_pos[0] += offset_x
            player_pos[1] += offset_y

        # shake do inimigo
        if self.enemy_hit_timer > 0:
            offset_x = random.randint(-self.enemy_shake_intensity, self.enemy_shake_intensity)
            offset_y = random.randint(-2, 2)
            enemy_pos[0] += offset_x
            enemy_pos[1] += offset_y

        # sombras
        self.draw_shadow(player_pos[0] + 20, player_pos[1] + 190, 150, 28)
        self.draw_shadow(enemy_pos[0] + 20, enemy_pos[1] + 190, 150, 28)

        # sprite do player com flash opcional
        player_sprite = self.player_sprite
        if self.player_flash_timer > 0 and player_sprite:
            player_sprite = self.apply_damage_flash(player_sprite, intensity=90)

        # sprite do inimigo com flash opcional
        enemy_sprite = self.enemy_sprite
        if self.enemy_flash_timer > 0 and enemy_sprite:
            enemy_sprite = self.apply_damage_flash(enemy_sprite, intensity=90)

        if player_sprite:
            self.screen.blit(player_sprite, player_pos)
        else:
            pygame.draw.rect(self.screen, (70, 120, 200), (140, 170, 140, 220))

        if enemy_sprite:
            self.screen.blit(enemy_sprite, enemy_pos)
        else:
            pygame.draw.rect(self.screen, (160, 70, 70), (720, 170, 140, 220))

        self.draw_player_xp_bar()

    def draw_floating_texts(self):
        for entry in self.floating_texts:
            text_surface = self.font.render(entry["text"], True, entry["color"])
            self.screen.blit(text_surface, (entry["x"], entry["y"]))

    def draw_shadow(self, x, y, width=150, height=28):
        shadow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 90), (0, 0, width, height))
        self.screen.blit(shadow_surface, (x, y))

    def draw_player_xp_bar(self):
        xp_x = 380
        xp_y = 65
        xp_width = 250
        xp_height = 10

        self.draw_bar(
            xp_x,
            xp_y,
            xp_width,
            xp_height,
            self.player.xp,
            self.player.xp_max,
            (100, 170, 60),
            bg_color=(30, 30, 30),
        )

        xp_text = self.small_font.render(
            f"XP: {self.player.xp}/{self.player.xp_max}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(xp_text, (xp_x + 28, xp_y + 14))

    def draw_bar(self, x, y, width, height, current, maximum, fill_color, bg_color=(35, 35, 35)):
        pygame.draw.rect(self.screen, bg_color, (x, y, width, height), border_radius=6)

        fill_width = int((current / maximum) * width) if maximum > 0 else 0

        if fill_width > 0:
            pygame.draw.rect(self.screen, fill_color, (x, y, fill_width, height), border_radius=6)

            highlight_height = max(2, height // 4)
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (x + 2, y + 2, max(0, fill_width - 4), highlight_height),
                border_radius=4,
            )

        pygame.draw.rect(self.screen, (190, 190, 190), (x, y, width, height), 2, border_radius=6)

    def get_hp_color(self, current, maximum):
        if maximum <= 0:
            return (190, 60, 60)

        ratio = current / maximum

        if ratio <= 0.25:
            return (200, 70, 70)
        elif ratio <= 0.50:
            return (220, 180, 70)
        return (60, 180, 90)

    def draw_hud(self):
        player_name = self.font.render(
            f"{self.player.name} Lv.{self.player.level}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(player_name, (120, 70))

        player_hp_color = self.get_hp_color(self.player.health, self.player.max_health)
        self.draw_bar(120, 105, 260, 22, self.player.health, self.player.max_health, player_hp_color)

        player_hp = self.small_font.render(
            f"HP {self.player.health}/{self.player.max_health}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(player_hp, (120, 132))

        self.draw_bar(120, 155, 260, 22, self.player.mana, self.player.mana_max, (70, 120, 220))
        player_mp = self.small_font.render(
            f"MP {self.player.mana}/{self.player.mana_max}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(player_mp, (120, 182))

        self.draw_status_effects(self.player, 120, 210)

        enemy_name = self.font.render(
            f"{self.monster.name} Lv.{self.monster.level}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(enemy_name, (650, 70))

        enemy_hp_color = self.get_hp_color(self.monster.health, self.monster.max_health)
        self.draw_bar(650, 105, 260, 22, self.monster.health, self.monster.max_health, enemy_hp_color)

        enemy_hp = self.small_font.render(
            f"HP {self.monster.health}/{self.monster.max_health}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(enemy_hp, (650, 132))

        self.draw_status_effects(self.monster, 650, 155)

    def draw_action_bar(self):
        bar_rect = pygame.Rect(120, 455, 760, 50)
        pygame.draw.rect(self.screen, (18, 18, 18), bar_rect, border_radius=10)
        pygame.draw.rect(self.screen, (160, 160, 160), bar_rect, 2, border_radius=10)

        x = 145
        y = 467

        for key, label in self.ACTIONS:
            key_surface = self.menu_font.render(key, True, (230, 210, 120))
            label_surface = self.menu_font.render(label, True, (240, 240, 240))

            self.screen.blit(key_surface, (x, y))
            self.screen.blit(label_surface, (x + 45, y))
            x += 145

    def draw_log_box(self):
        margin = 50
        box_height = 150
        padding_x = 20
        padding_y = 15
        line_spacing = 5

        log_rect = pygame.Rect(
            margin,
            self.height - box_height - 20,
            self.width - margin * 2,
            box_height,
        )

        pygame.draw.rect(self.screen, (15, 15, 15), log_rect, border_radius=8)
        pygame.draw.rect(self.screen, (150, 150, 150), log_rect, 2, border_radius=8)

        x = log_rect.x + padding_x
        y = log_rect.y + padding_y
        max_width = log_rect.width - (padding_x * 2)

        rendered_lines = []
        for entry in self.state.log_messages:
            rendered_lines.extend(self.wrap_text(entry["text"], self.small_font, max_width))

        line_height = self.small_font.get_height() + line_spacing
        max_lines = (log_rect.height - (padding_y * 2)) // line_height
        rendered_lines = rendered_lines[-max_lines:]

        for line in rendered_lines:
            text_surface = self.small_font.render(line, True, (230, 230, 230))
            self.screen.blit(text_surface, (x, y))
            y += line_height

    def draw_status_effects(self, entity, x, y):
        if not hasattr(entity, "status_effects") or not entity.status_effects:
            return

        badge_x = x
        badge_y = y
        badge_width = 72
        badge_height = 22
        gap = 8

        label_map = {
            "poison": "POI",
            "guard": "GRD",
            "bleed": "BLD",
            "burn": "BRN",
            "stun": "STN",
        }

        color_map = {
            "poison": (80, 170, 90),
            "guard": (80, 140, 220),
            "bleed": (180, 70, 70),
            "burn": (220, 120, 60),
            "stun": (190, 170, 70),
        }

        for effect in entity.status_effects[:3]:
            effect_type = effect.get("type", "status").lower()
            duration = effect.get("duration", 0)
            short_label = label_map.get(effect_type, effect_type[:3].upper())
            border_color = color_map.get(effect_type, (110, 110, 110))

            text_label = f"{short_label} {duration}"

            rect = pygame.Rect(badge_x, badge_y, badge_width, badge_height)
            pygame.draw.rect(self.screen, (24, 24, 24), rect, border_radius=6)
            pygame.draw.rect(self.screen, border_color, rect, 1, border_radius=6)

            text_surface = self.small_font.render(text_label, True, (220, 220, 220))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

            badge_x += badge_width + gap
    # =========================
    # Hit Effects
    # =========================
    def trigger_enemy_hit_effect(self, duration=10, flash_duration=6, shake_intensity=10):
        self.enemy_hit_timer = duration
        self.enemy_flash_timer = flash_duration
        self.enemy_shake_intensity = shake_intensity
        
    def trigger_player_hit_effect(self, duration=10, flash_duration=6, shake_intensity=8):
        self.player_hit_timer = duration
        self.player_flash_timer = flash_duration
        self.player_shake_intensity = shake_intensity


    # =========================
    # Revive overlay
    # =========================

    def open_revive_prompt(self):
        self.state.show_menu = False
        self.state.show_inventory = False
        self.state.show_equipped = False
        self.state.show_skills = False
        self.state.show_potions = False
        self.state.show_zone_menu = False

        self.state.show_revive_prompt = True
        self.state.revive_penalty_preview = self.player.preview_death_penalty(0.20)

        preview = self.state.revive_penalty_preview
        self.add_log(
            f"{self.player.name} was defeated. Revive will cost {preview['xp_loss']} XP.",
            LOG_IMPORTANT
        )

        if preview["will_level_down"]:
            self.add_log("This penalty can reduce your level.", LOG_IMPORTANT)

    def confirm_revive(self):
        penalty = self.player.apply_death_penalty(0.20)

        self.player.health = self.player.max_health
        self.player.mana = self.player.mana_max

        self.battle.run_from_battle()
        self.sync_entities()
        self.battle.set_player_turn()

        self.state.show_revive_prompt = False
        self.state.revive_penalty_preview = None

        self.add_log(
            f"{self.player.name} revived and lost {penalty['xp_loss']} XP.",
            LOG_IMPORTANT
        )

        if penalty["level_down"]:
            self.add_log(
                f"Level reduced: {penalty['old_level']} -> {penalty['new_level']}.",
                LOG_IMPORTANT
            )

        self.show_battle_cry()

    def handle_revive_input(self, event):
        if event.key == pygame.K_RETURN:
            self.confirm_revive()
        elif event.key == pygame.K_ESCAPE:
            return
    
    # =========================
    # Loop principal
    # =========================
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_input(event)

            self.update_floating_texts()
            self.update_zone_transition()
            self.update_hit_effects()
            self.update_pending_battle_actions()
            self.draw()
            self.clock.tick(120)

        pygame.quit()