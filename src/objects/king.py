import pygame
from objects.cats import BaseCat
from objects.tiles import all_sprites


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, initial_health_percentage, hp):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.initial_health_percentage = initial_health_percentage
        self.current_health_percentage = initial_health_percentage
        self.max_hp = hp

        self.font = pygame.font.Font(None, 30)
        self.text_hp_string_rendered = None
        self.text_hp_rect = None
        self.text_wave_string_rendered = None
        self.text_wave_rect = None
        self.text_level_string_rendered = None
        self.text_level_rect = None
        self.text_time_before_wave_string_rendered = None
        self.text_time_before_wave_rect = None

    def update(self, new_health_percentage):
        self.current_health_percentage = new_health_percentage
        self.draw_health_bar()
        self.update_hp_text()

    def draw_health_bar(self):
        self.image.fill((0, 0, 0))
        green_width = int(self.width * self.current_health_percentage)
        gray_width = self.width - green_width
        pygame.draw.rect(self.image, (230, 0, 0), (0, 0, green_width, self.height))
        pygame.draw.rect(self.image, (169, 169, 169), (green_width, 0, gray_width, self.height))

    def update_hp_text(self):
        hp = self.max_hp * self.current_health_percentage
        self.text_hp_string_rendered = self.font.render(f"HP: {int(hp)}", 1, pygame.Color('white'))
        self.text_hp_rect = self.text_hp_string_rendered.get_rect(
            center=(self.rect.center[0], self.rect.center[1] + 2))

    def update_wave_text(self, wave):
        self.text_wave_string_rendered = self.font.render(f"Wave: {wave}", 1, pygame.Color('black'))
        self.text_wave_rect = self.text_wave_string_rendered.get_rect(
            center=(self.rect.center[0], self.rect.center[1] + self.rect.height + 5))

    def update_time_before_wave(self, time):
        self.text_time_before_wave_string_rendered = self.font.render(f"Time before wave: {time}", 1,
                                                                      pygame.Color('black'))
        self.text_time_before_wave_rect = self.text_wave_string_rendered.get_rect(
            center=(self.rect.center[0] - 65, self.rect.center[1] + 2 * self.rect.height + 5))

    def update_level_text(self, level):
        self.text_level_string_rendered = self.font.render(f"Level: {level}", 1, pygame.Color('black'))
        self.text_level_rect = self.text_level_string_rendered.get_rect(
            center=(self.rect.center[0], self.rect.center[1] - self.rect.height - 5))


class King(BaseCat):
    def __init__(self, pos_x, pos_y, cat_images, hp):
        super().__init__(pos_x, pos_y, "king", cat_images)
        self.hp = self.max_hp = hp
        self.hp_bar = HealthBar(50, 50, 500, 20, 1, self.hp)
