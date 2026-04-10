import os
import pygame

from player.knight import Knight
from player.archer import Archer
from player.thief import Thief
from player.mage import Mage


class CharacterCreationScreen:
    def __init__(self, width=1000, height=700):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Knightfall - Character Creation")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("arial", 22)

        self.running = True
        self.selected_index = 0
        self.player_name = ""
        self.typing_name = True
        self.created_player = None

        self.classes = [
            {"label": "Knight", "class": Knight, "sprite": self.load_sprite("knight")},
            {"label": "Archer", "class": Archer, "sprite": self.load_sprite("archer")},
            {"label": "Thief", "class": Thief, "sprite": self.load_sprite("thief")},
            {"label": "Mage", "class": Mage, "sprite": self.load_sprite("mage")},
        ]

    def load_sprite(self, name, size=(140, 140)):
        path = os.path.join("assets", "player", f"{name}.png")

        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(image, size)

        return None

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.typing_name:
            if event.key == pygame.K_RETURN:
                if self.player_name.strip():
                    self.typing_name = False
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                if len(self.player_name) < 16 and event.unicode.isprintable():
                    self.player_name += event.unicode
            return

        if event.key == pygame.K_LEFT:
            self.selected_index = max(0, self.selected_index - 1)

        elif event.key == pygame.K_RIGHT:
            self.selected_index = min(len(self.classes) - 1, self.selected_index + 1)

        elif event.key == pygame.K_RETURN:
            selected = self.classes[self.selected_index]
            name = self.player_name.strip() or selected["label"]
            self.created_player = selected["class"](name)
            self.running = False

    def draw_background(self):
        self.screen.fill((10, 10, 10))

    def draw_title(self):
        title = self.font.render("Choose Your Class", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 40))

    def draw_name_input(self):
        label = self.small_font.render("Name:", True, (220, 220, 220))
        self.screen.blit(label, (100, 110))

        input_rect = pygame.Rect(180, 105, 300, 40)
        pygame.draw.rect(self.screen, (20, 20, 20), input_rect, border_radius=8)
        pygame.draw.rect(self.screen, (180, 180, 180), input_rect, 2, border_radius=8)

        text = self.small_font.render(self.player_name or "Type your name...", True, (255, 255, 255))
        self.screen.blit(text, (195, 114))

        hint = "Press ENTER to confirm name" if self.typing_name else "Use LEFT/RIGHT and ENTER to choose class"
        hint_surface = self.small_font.render(hint, True, (180, 180, 180))
        self.screen.blit(hint_surface, (100, 160))

    def draw_classes(self):
        start_x = 90
        gap = 210
        y = 250

        for index, class_data in enumerate(self.classes):
            x = start_x + (index * gap)
            card_rect = pygame.Rect(x, y, 170, 240)

            selected = index == self.selected_index and not self.typing_name
            border_color = (220, 190, 80) if selected else (120, 120, 120)

            pygame.draw.rect(self.screen, (20, 20, 20), card_rect, border_radius=12)
            pygame.draw.rect(self.screen, border_color, card_rect, 3, border_radius=12)

            if class_data["sprite"]:
                sprite_rect = class_data["sprite"].get_rect(center=(x + 85, y + 85))
                self.screen.blit(class_data["sprite"], sprite_rect)
            else:
                pygame.draw.rect(self.screen, (70, 70, 120), (x + 35, y + 20, 100, 100), border_radius=8)

            label = self.font.render(class_data["label"], True, (255, 255, 255))
            self.screen.blit(label, (x + 85 - label.get_width() // 2, y + 150))

            choose_text = "Selected" if selected else "Available"
            status = self.small_font.render(choose_text, True, border_color)
            self.screen.blit(status, (x + 85 - status.get_width() // 2, y + 195))

    def draw(self):
        self.draw_background()
        self.draw_title()
        self.draw_name_input()
        self.draw_classes()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                self.handle_input(event)

            self.draw()
            self.clock.tick(60)

        return self.created_player