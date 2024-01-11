import pygame
from pygame.sprite import Sprite


class BaseCard:
    def __init__(self, x, y, button_text, name_text, custom_image=None):
        self.x = x
        self.y = y
        self.counter = 0
        self.image = pygame.Surface((32 + 26, 32 + 28))  # Увеличиваем ширину и высоту для счетчика
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.name = self.Name(self, name_text)
        self.button = self.Button(self, button_text)
        self.counter_display = self.CounterDisplay(self)
        self.custom_image = None
        if custom_image:
            self.custom_image = self.Image(self, custom_image)

    class Name:
        def __init__(self, outer_instance, text):
            self.outer_instance = outer_instance
            self.font = pygame.font.Font(None, 16)
            self.text = text
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            self.rect = self.rendered_text.get_rect(midtop=(outer_instance.x, outer_instance.y))

        def draw(self, screen):
            screen.blit(self.rendered_text, self.rect)

    class Image:
        def __init__(self, outer_instance, image):
            self.outer_instance = outer_instance
            self.image = image
            self.rect = self.image.get_rect(midtop=(outer_instance.x, outer_instance.y + 16))

        def draw(self, screen):
            screen.blit(self.image, self.rect)

    class Button(Sprite):
        def __init__(self, outer_instance, text):
            super().__init__()
            self.outer_instance = outer_instance
            self.image = pygame.Surface((48 + 4, 16 + 4))  # Увеличиваем ширину и высоту кнопки
            self.image.fill((150, 150, 150))
            self.rect = self.image.get_rect(midtop=(outer_instance.x - 4, outer_instance.y + 84))  # Смещаем кнопку вниз
            self.font = pygame.font.Font(None, 18)
            self.text = text
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            self.text_rect = self.rendered_text.get_rect(midleft=self.rect.center)
            self.mini_image = pygame.Surface((16, 16))  # Уменьшаем размер мини-изображения
            self.mini_image.fill((255, 0, 0))
            self.mini_image_rect = self.mini_image.get_rect(midleft=(self.rect.x + 4, self.rect.y + 10))

        def draw(self, screen):
            screen.blit(self.image, self.rect)
            screen.blit(self.rendered_text, self.text_rect)
            screen.blit(self.mini_image, self.mini_image_rect)

        def update(self):
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()[0]

            if self.rect.collidepoint(mouse_pos):
                if click:
                    self.outer_instance.counter += 1

    class CounterDisplay:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.font = pygame.font.Font(None, 24)
            self.text = str(outer_instance.counter)
            self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
            self.rect = self.rendered_text.get_rect(midtop=(outer_instance.x + 26, outer_instance.y + 84))

        def draw(self, screen):
            screen.blit(self.rendered_text, self.rect)

# Пример использования
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

custom_image = pygame.Surface((64, 64))
custom_image.fill((255, 0, 0))

card = BaseCard(x=50, y=50, button_text="100", name_text="Котоимя", custom_image=custom_image)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    card.button.update()

    screen.fill((255, 255, 255))
    card.button.draw(screen)
    if card.custom_image:
        card.custom_image.draw(screen)
    card.name.draw(screen)
    card.counter_display.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
