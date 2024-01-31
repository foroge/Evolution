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

    def draw(self, screen):
        self.menu_button.draw(screen)

    def update(self):
        stat_upd = self.menu_button.update()
        return stat_upd