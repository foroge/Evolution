import pygame
from pygame.sprite import Sprite
from src.load.load_images import load_image

card_gr = pygame.sprite.Group()


class BaseCard:
    def __init__(self, x, y, button_text, name_text, custom_image=None):
        self.x = x
        self.y = y
        self.counter = 0
        self.image = pygame.Surface((32 + 26, 32 + 28))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect().move(x, y)

        self.name = self.Name(self, name_text)
        self.button = self.ButtonBuy(self, button_text)
        self.button_choose = self.ButtonChoose(self, "Choose")
        self.counter_display = self.CounterDisplay(self)
        self.custom_image = None
        if custom_image:
            self.custom_image = self.Image(self, custom_image)

    class Name:
        def __init__(self, outer_instance, text):
            self.outer_instance = outer_instance
            self.font = pygame.font.Font(None, 20)
            self.text = text
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            x = self.outer_instance.x
            y = self.outer_instance.y
            self.rect = self.rendered_text.get_rect(center=(x + 40, y))

        def draw(self, screen):
            screen.blit(self.rendered_text, self.rect)

    class Image:
        def __init__(self, outer_instance, image):
            self.outer_instance = outer_instance
            self.image = image
            self.scale((80, 80))
            self.rect = self.image.get_rect().move(outer_instance.x, outer_instance.y + 20)

        def draw(self, screen):
            screen.blit(self.image, self.rect)

        def scale(self, size):
            self.image = pygame.transform.scale(self.image, size)

    class ButtonBuy(Sprite):
        def __init__(self, outer_instance, text):
            super().__init__()
            self.outer_instance = outer_instance
            self.image = pygame.Surface((56, 20))
            self.image.fill((150, 150, 150))
            x = self.outer_instance.x
            self.handled = False
            y = self.outer_instance.y + 106
            self.rect = self.image.get_rect().move(x, y)  # Смещаем кнопку вниз

            self.font = pygame.font.Font(None, 18)
            self.text = text

            self.mini_image = load_image("other_images/coin.png")
            self.mini_image_rect = self.mini_image.get_rect().move(self.rect.x + 4, self.rect.y + 2)
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            x = self.mini_image_rect.x + self.mini_image_rect.width
            self.text_rect = self.rendered_text.get_rect(midleft=(x, self.rect.center[1]))

        def draw(self, screen):
            screen.blit(self.image, self.rect)
            screen.blit(self.rendered_text, self.text_rect)
            screen.blit(self.mini_image, self.mini_image_rect)

        def update(self):
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()[0]
            if click and self.rect.collidepoint(mouse_pos):
                if not self.handled:
                    self.handled = True
                    self.outer_instance.counter += 1
            else:
                self.handled = False

    class ButtonChoose(Sprite):
        def __init__(self, outer_instance, text):
            super().__init__()
            self.outer_instance = outer_instance
            self.image = pygame.Surface((80, 20))
            self.image.fill((150, 150, 150))
            x = self.outer_instance.x
            y = self.outer_instance.y + 136
            self.rect = self.image.get_rect().move(x, y)  # Смещаем кнопку вниз
            self.handled = False

            self.font = pygame.font.Font(None, 18)
            self.text = text
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

        def draw(self, screen):
            screen.blit(self.image, self.rect)
            screen.blit(self.rendered_text, self.text_rect)

        def update(self):
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()[0]
            if click and self.rect.collidepoint(mouse_pos):
                if not self.handled:
                    self.handled = True
                    return self.outer_instance.name.text
            else:
                self.handled = False

    class CounterDisplay:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.font = pygame.font.Font(None, 24)
            self.text = str(self.outer_instance.counter)
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            x = self.outer_instance.x + self.outer_instance.button.rect.size[0] + 5
            y = self.outer_instance.y + 108
            self.rect = self.rendered_text.get_rect().move(x, y)

        def draw(self, screen):
            self.text = str(self.outer_instance.counter)
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            x = self.outer_instance.x + self.outer_instance.button.rect.size[0] + 5
            y = self.outer_instance.y + 108
            self.rect = self.rendered_text.get_rect().move(x, y)
            screen.blit(self.rendered_text, self.rect)

    def all_draw(self, screen):
        self.name.draw(screen)
        self.button.draw(screen)
        self.button_choose.draw(screen)
        self.counter_display.draw(screen)
        self.custom_image.draw(screen)
