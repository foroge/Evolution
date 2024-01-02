import pygame


def change_size_sprites(sprites, scale):
    for sprite in sprites:
        sprite.change_size(scale)


def sptires_move(sprites, vx, vy):
    for sprite in sprites:
        sprite.move(vx, vy)


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
        self.scale = 1
        self.step = 0.02

    def change_scale(self, flag):
        if flag and self.scale >= full_h - 60:
            self.scale += self.step
        else:
            self.scale -= self.step