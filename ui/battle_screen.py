import pygame
from ui.battle_ui_state import BattleUIState
from battle.battle_inventory import BattleInventory
import os
import pygame

class BattleScreen:
    def __init__(self, battle, width=1000, height=700):
        pygame.init()

        self.battle = battle
        self.player = battle.player
        self.monster = battle.monster
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.menu_font = pygame.font.SysFont("arial", 28, bold=True)

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Knightfall")
        self.show_skills = False
        self.skill_index = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.player_sprite = self.load_sprite("player", self.get_player_sprite_name())
        self.enemy_sprite = self.load_sprite("enemies", self.monster.name)
        self.background = pygame.image.load("assets/background/battle_bg.png").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.floating_texts = []
        self.running = True
        self.state = BattleUIState()
        self.show_battle_cry()


    #SPRITES LOAD
    def load_sprite(self, folder, name, size=(250, 250)):
        filename = f"{self.normalize_name(name)}.png"
        path = os.path.join("assets", folder, filename)

        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, size)
            return image

        return None

    def get_player_sprite_name(self):
        class_map = {
            1: "knight",
            2: "archer",
            3: "thief",
            4: "mage"
        }
        return class_map.get(self.player.class_type, "knight")

    def normalize_name(self, name):
        return name.lower().replace(" ", "_")
    
    def add_log(self, text):
        self.state.add_log(text)

    def event(self, text, delay=0):
        self.add_log(text)

    def sync_entities(self):
        self.player = self.battle.player
        self.monster = self.battle.monster

        self.player_sprite = self.load_sprite("player", self.get_player_sprite_name())
        self.enemy_sprite = self.load_sprite("enemies", self.monster.name)

    def show_battle_cry(self):
        if hasattr(self.monster, "battle_cry"):
            cry = self.monster.battle_cry()
            if cry:
                self.add_log(cry)

    def add_floating_text(self, text, x, y, color=(255, 80, 80), duration=45):
        self.floating_texts.append({
            "text": str(text),
            "x": x,
            "y": y,
            "color": color,
            "duration": duration
        })

    def update_floating_texts(self):
        for entry in self.floating_texts:
            entry["y"] -= 1
            entry["duration"] -= 1

        self.floating_texts = [entry for entry in self.floating_texts if entry["duration"] > 0]
    
    def draw_floating_texts(self):
        for entry in self.floating_texts:
            text_surface = self.font.render(entry["text"], True, entry["color"])
            self.screen.blit(text_surface, (entry["x"], entry["y"]))

    def get_bag_items(self):
        return BattleInventory.get_bag_items(self.player)
    
    def get_potion_items(self):
        items = []

        if self.player.healpotions > 0:
            items.append({
                "name": "Heal Potion",
                "quantity": self.player.healpotions,
                "kind": "heal_potion"
            })

        if self.player.manapotions > 0:
            items.append({
                "name": "Mana Potion",
                "quantity": self.player.manapotions,
                "kind": "mana_potion"
            })

        return items

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

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.state.show_bag:
            self.handle_bag_input(event)
            return

        if event.key == pygame.K_1:
            self.battle.actions.attack()

        elif event.key == pygame.K_2:
            self.state.show_skills = True
            self.state.skill_index = 0
        
        if self.state.show_skills:
            self.handle_skill_input(event)
            return

        elif event.key == pygame.K_3:
            self.state.show_bag = True
            self.state.bag_index = 0

        elif event.key == pygame.K_4:
            self.battle.actions.run()

    def draw_background(self):
        if hasattr(self, "background") and self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((10, 10, 10))

    def draw_battle_area(self):
        player_pos = (200, 230)
        enemy_pos = (640, 230)

        if self.player_sprite:
            self.screen.blit(self.player_sprite, player_pos)
        else:
            pygame.draw.rect(self.screen, (70, 120, 200), (140, 170, 140, 220))

        if self.enemy_sprite:
            self.screen.blit(self.enemy_sprite, enemy_pos)
        else:
            pygame.draw.rect(self.screen, (160, 70, 70), (720, 170, 140, 220))

    def get_inventory_categories(self):
        return ["weapon", "shield", "armor", "helmet", "jewel", "misc"]
    
    def get_menu_options(self):
       return ["Bag", "Equipped", "Close"]

    def draw_potions_overlay(self):
        overlay = pygame.Rect(180, 120, 640, 420)
        pygame.draw.rect(self.screen, (20, 20, 20), overlay)
        pygame.draw.rect(self.screen, (200, 200, 200), overlay, 2)

        title = self.font.render("Potions", True, (255, 255, 255))
        self.screen.blit(title, (445, 140))

        items = self.get_potion_items()

        if not items:
            text = self.small_font.render("No potions available.", True, (220, 220, 220))
            self.screen.blit(text, (240, 200))
        else:
            y = 200
            for index, item in enumerate(items):
                prefix = ">" if index == self.state.potion_index else " "
                line = f"{prefix} {item['name']} x{item['quantity']}"
                text = self.small_font.render(line, True, (220, 220, 220))
                self.screen.blit(text, (240, y))
                y += 30

        footer = self.small_font.render("[ENTER] Use   [ESC] Close", True, (180, 180, 180))
        self.screen.blit(footer, (240, 500))
    def draw_bar(self, x, y, width, height, current, maximum, fill_color, bg_color=(35, 35, 35)):
        pygame.draw.rect(self.screen, bg_color, (x, y, width, height), border_radius=6)

        if maximum > 0:
            fill_width = int((current / maximum) * width)
        else:
            fill_width = 0

        if fill_width > 0:
            pygame.draw.rect(
                self.screen,
                fill_color,
                (x, y, fill_width, height),
                border_radius=6
            )

            highlight_height = max(2, height // 4)
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (x + 2, y + 2, max(0, fill_width - 4), highlight_height),
                border_radius=4
            )

        pygame.draw.rect(self.screen, (190, 190, 190), (x, y, width, height), 2, border_radius=6)

    def draw_hud(self):
        player_name = self.font.render(
            f"{self.player.name} Lv.{self.player.level}", True, (255, 255, 255)
        )
        self.screen.blit(player_name, (120, 70))

        self.draw_bar(120, 105, 260, 22, self.player.health, self.player.max_health, (60, 180, 90))
        player_hp = self.small_font.render(
            f"HP {self.player.health}/{self.player.max_health}", True, (255, 255, 255)
        )
        self.screen.blit(player_hp, (120, 132))

        self.draw_bar(120, 155, 260, 22, self.player.mana, self.player.mana_max, (70, 120, 220))
        player_mp = self.small_font.render(
            f"MP {self.player.mana}/{self.player.mana_max}", True, (255, 255, 255)
        )
        self.screen.blit(player_mp, (120, 182))

        enemy_name = self.font.render(
            f"{self.monster.name} Lv.{self.monster.level}", True, (255, 255, 255)
        )
        self.screen.blit(enemy_name, (650, 70))

        self.draw_bar(650, 105, 260, 22, self.monster.health, self.monster.max_health, (190, 60, 60))
        enemy_hp = self.small_font.render(
            f"HP {self.monster.health}/{self.monster.max_health}", True, (255, 255, 255)
        )
        self.screen.blit(enemy_hp, (650, 132))

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
                    # caso raro: palavra sozinha maior que max_width
                    lines.append(word)

        if current_line:
            lines.append(current_line)

        return lines

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
            box_height
        )

        pygame.draw.rect(self.screen, (15, 15, 15), log_rect, border_radius=8)
        pygame.draw.rect(self.screen, (150, 150, 150), log_rect, 2, border_radius=8)

        x = log_rect.x + padding_x
        y = log_rect.y + padding_y
        max_width = log_rect.width - (padding_x * 2)

        rendered_lines = []

        for entry in self.state.logs:
            wrapped_lines = self.wrap_text(str(entry), self.small_font, max_width)
            rendered_lines.extend(wrapped_lines)

        line_height = self.small_font.get_height() + line_spacing
        max_lines = (log_rect.height - (padding_y * 2)) // line_height

        rendered_lines = rendered_lines[-max_lines:]

        for line in rendered_lines:
            text_surface = self.small_font.render(line, True, (230, 230, 230))
            self.screen.blit(text_surface, (x, y))
            y += line_height

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

            if selected == "Bag":
                self.state.show_menu = False
                self.state.show_inventory = True
                self.state.inventory_category_index = 0
                self.state.inventory_item_index = 0

            elif selected == "Equipped":
                self.state.show_menu = False
                self.state.show_equipped = True

            elif selected == "Close":
                self.state.show_menu = False

    def draw_action_bar(self):
        bar_rect = pygame.Rect(120, 455, 760, 50)
        pygame.draw.rect(self.screen, (18, 18, 18), bar_rect, border_radius=10)
        pygame.draw.rect(self.screen, (160, 160, 160), bar_rect, 2, border_radius=10)

        actions = [
            ("[1]", "Attack"),
            ("[2]", "Skill"),
            ("[3]", "Potions"),
            ("[4]", "Run"),
            ("[5]", "Menu"),
        ]

        x = 145
        y = 467

        for key, label in actions:
            key_surface = self.menu_font.render(key, True, (230, 210, 120))
            label_surface = self.menu_font.render(label, True, (240, 240, 240))

            self.screen.blit(key_surface, (x, y))
            self.screen.blit(label_surface, (x + 45, y))

            x += 145

    def draw_bag_overlay(self):
        overlay = pygame.Rect(180, 120, 640, 420)
        pygame.draw.rect(self.screen, (20, 20, 20), overlay)
        pygame.draw.rect(self.screen, (200, 200, 200), overlay, 2)

        title = self.font.render("Bag", True, (255, 255, 255))
        self.screen.blit(title, (470, 140))

        items = self.get_bag_items()

        if not items:
            text = self.small_font.render("Bag is empty.", True, (220, 220, 220))
            self.screen.blit(text, (240, 200))
        else:
            y = 200
            for index, item in enumerate(items):
                prefix = ">" if index == self.state.bag_index else " "

                if isinstance(item, dict):
                    line = f"{prefix} {item['name']} x{item['quantity']}"
                else:
                    line = f"{prefix} {item.name} x{getattr(item, 'quantity', 1)}"

                text = self.small_font.render(line, True, (220, 220, 220))
                self.screen.blit(text, (240, y))
                y += 28

        footer = self.small_font.render("[ENTER] Use   [ESC] Close", True, (180, 180, 180))
        self.screen.blit(footer, (240, 500))

    def draw_skill_overlay(self):
        overlay = pygame.Rect(180, 120, 640, 420)
        pygame.draw.rect(self.screen, (20, 20, 20), overlay)
        pygame.draw.rect(self.screen, (200, 200, 200), overlay, 2)

        title = self.font.render("Skills", True, (255, 255, 255))
        self.screen.blit(title, (455, 140))

        skills = self.player.skills

        if not skills:
            text = self.small_font.render("No skills available.", True, (220, 220, 220))
            self.screen.blit(text, (240, 200))
        else:
            y = 200
            for index, skill in enumerate(skills):
                prefix = ">" if index == self.state.skill_index else " "
                line = f"{prefix} {skill['name']} | MP: {skill['mana_cost']} | {skill['description']}"
                text = self.small_font.render(line, True, (220, 220, 220))
                self.screen.blit(text, (240, y))
                y += 28

        footer = self.small_font.render("[ENTER] Use   [ESC] Close", True, (180, 180, 180))
        self.screen.blit(footer, (240, 500))

    def draw(self):
        self.draw_background()
        self.draw_battle_area()
        self.draw_hud()
        self.draw_action_bar()
        self.draw_log_box()
        self.draw_floating_texts()

        if self.state.show_bag:
            self.draw_bag_overlay()

        if self.state.show_skills:
            self.draw_skill_overlay()

        pygame.display.flip()

    def draw_menu_overlay(self):
        overlay = pygame.Rect(300, 160, 400, 300)
        pygame.draw.rect(self.screen, (20, 20, 20), overlay)
        pygame.draw.rect(self.screen, (200, 200, 200), overlay, 2)

        title = self.font.render("Menu", True, (255, 255, 255))
        self.screen.blit(title, (460, 185))

        options = self.get_menu_options()
        y = 250

        for index, option in enumerate(options):
            prefix = ">" if index == self.state.menu_index else " "
            line = f"{prefix} {option}"
            color = (230, 210, 120) if index == self.state.menu_index else (220, 220, 220)

            text = self.font.render(line, True, color)
            self.screen.blit(text, (380, y))
            y += 50

        footer = self.small_font.render("[ENTER] Select   [ESC] Close", True, (180, 180, 180))
        self.screen.blit(footer, (360, 420))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            self.update_floating_texts()
            self.draw()
            self.clock.tick(120)

        pygame.quit()