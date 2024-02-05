import pygame
from extra_utils import Button


class LoseMenu:
    def __init__(self, x, y):
        self.full_x = x
        self.full_y = y
        self.x = x // 2
        self.y = y // 2
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        button_size = (150, 50)
        self.restart_button = Button(self.full_x - 2 * (button_size[0] + 10), self.full_y - button_size[1] - 10,
                                     *button_size, "Restart", "white")
        self.menu_button = Button(self.full_x - button_size[0] - 10, self.full_y - button_size[1] - 10,
                                  *button_size, "Back to menu", "white")

    def update(self):
        menu_upd = self.menu_button.update()
        restart_upd = self.restart_button.update()
        return menu_upd, restart_upd

    def draw(self, screen):
        self.menu_button.draw(screen)
        self.restart_button.draw(screen)

