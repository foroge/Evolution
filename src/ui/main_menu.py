import pygame
from extra_utils import Button


class MainMenu:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.title_text = self.TitleText(self)
        button_size = (150, 50)
        self.new_game_button = Button(self.x - button_size[0] // 2, self.y - button_size[1] // 2, *button_size,
                                    "New game", "white")
        self.exit_button = Button(self.x - button_size[0] // 2, self.y - button_size[1] // 2 + 75, *button_size,
                                  "Exit", "white")

    class TitleText:
        def __init__(self, outer_instance):
            self.font = pygame.font.Font(None, 72)
            self.outer_instance = outer_instance
            self.text = "Feline fortress"
            self.rendered_text = self.font.render(self.text, True, "white")
            x = self.outer_instance.x
            y = self.outer_instance.y
            self.rect = self.rendered_text.get_rect(center=(x, y - 100))

        def draw(self, screen):
            screen.blit(self.rendered_text, self.rect)

    def draw(self, screen):
        self.title_text.draw(screen)
        self.new_game_button.draw(screen)
        self.exit_button.draw(screen)

    def update(self):
        new_game_upd = self.new_game_button.update()
        ext_upd = self.exit_button.update()
        return new_game_upd, ext_upd