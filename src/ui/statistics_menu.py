import pygame
from data_base.data_base import DataBase
from extra_utils import Button


class StatisticsMenu:
    def __init__(self, x, y):
        self.full_x = x
        self.full_y = y
        self.x = x // 2
        self.y = y // 2
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        button_size = (150, 50)
        self.menu_button = Button(self.full_x - button_size[0] - 10, self.full_y - button_size[1] - 10,
                                  *button_size, "Back to menu", "white")

    class DBViewer:
        def __init__(self, outer_instance):
            self.font = pygame.font.Font(None, 72)
            self.outer_instance = outer_instance
            self.data = DataBase()
            self.font = pygame.font.SysFont(None, 30)
            self.rendered_text = self.font.render(self.text, True, "white")
            x = self.outer_instance.x
            y = self.outer_instance.y
            self.rect = self.rendered_text.get_rect(center=(x, y - 100))

        def draw(self, screen):
            pass

    def draw(self, screen):
        self.menu_button.draw(screen)

    def update(self):
        menu_upd = self.menu_button.update()
        if menu_upd:
            return 2