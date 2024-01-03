import pygame


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def change_size_sprites(sprites, scale):
    for sprite in sprites:
        sprite.change_size(scale)


def sptires_move(sprites, vx, vy, horizontal_borders, vertical_borders):
    for sprite in sprites:
        sprite.update(vx, vy, horizontal_borders, vertical_borders)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2 - 20:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([20, y2 - y1])
            self.image.fill((0, 0, 0))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 20])
            self.image.fill((0, 0, 0))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
# class CustomSpriteGroup(pygame.sprite.Group):
#     def __init__(self, *sprites):
#         super().__init__(*sprites)
#         self.collision = False
#
#     def update(self, wall):
#         super().update()
#         for sprite in self.sprites():


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.scale = 0.65
        self.step = 0.02

    def change_scale(self, flag):
        if flag and self.scale <= 1.2:
            self.scale += self.step
        elif not flag and self.scale >= 0.5:
            self.scale -= self.step