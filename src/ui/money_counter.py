import pygame

from load.load_images import load_image


class MoneyCounter:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.count = 100

        self.font = pygame.font.Font(None, 32)
        self.text = str(self.count)
        self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
        self.rect = self.rendered_text.get_rect(topright=(self.x, self.y))

        self.mini_image = load_image("other_images/coin.png")
        self.mini_image_rect = self.mini_image.get_rect(topleft=(self.x + 6, self.y + 2))

    def draw(self, screen):
        self.text = str(self.count)
        self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
        self.rect = self.rendered_text.get_rect(topright=(self.x, self.y))
        self.mini_image_rect = self.mini_image.get_rect(topleft=(self.x + 6, self.y + 2))
        screen.blit(self.rendered_text, self.rect)
        screen.blit(self.mini_image, self.mini_image_rect)