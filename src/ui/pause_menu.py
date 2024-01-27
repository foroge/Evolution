import pygame
from extra_utils import Button


class PauseMenu:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.pause_text = self.PauseText(self)
        button_size = (150, 50)
        self.resume_button = Button(self.x - button_size[0] // 2, self.y - button_size[1] // 2, *button_size, "Resume game", "white")
        self.exit_button = Button(self.x - button_size[0] // 2, self.y - button_size[1] // 2 + 75, *button_size, "Exit game", "white")

    class PauseText:
        def __init__(self, outer_instance):
            self.font = pygame.font.Font(None, 72)
            self.outer_instance = outer_instance
            self.text = "Paused"
            self.rendered_text = self.font.render(self.text, True, "white")
            x = self.outer_instance.x
            y = self.outer_instance.y
            self.rect = self.rendered_text.get_rect(center=(x, y - 100))

        def draw(self, screen):
            screen.blit(self.rendered_text, self.rect)

    def draw(self, screen):
        self.pause_text.draw(screen)
        self.resume_button.draw(screen)
        self.exit_button.draw(screen)

    def update(self):
        res_upd = self.resume_button.update()
        ext_upd = self.exit_button.update()
        return not res_upd, not ext_upd
