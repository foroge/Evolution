import pygame
from data_base.data_base import DataBase, DBViewer
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
        self.delete_button = Button(self.full_x - button_size[0] - 10, 10,
                                    *button_size, "Delete all stat.", "white")
        self.menu_button = Button(self.full_x - button_size[0] - 10, self.full_y - button_size[1] - 10,
                                  *button_size, "Back to menu", "white")
        self.db_view = DBViewer(40, 40, self.full_x, self.full_y)

        self.pos_y = 0

    def draw(self, screen):
        self.db_view.draw(screen, y=self.pos_y)
        self.menu_button.draw(screen)
        self.delete_button.draw(screen)

    def scroll(self, flag):
        if not flag and self.db_view.get_y_size() + self.pos_y > self.full_y:
            self.pos_y -= 50
        elif flag and self.pos_y <= -50:
            self.pos_y += 50

    def update(self):
        stat_upd = self.menu_button.update()
        if self.delete_button.update():
            self.db_view.db.del_all()
        return stat_upd
