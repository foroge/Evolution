import pygame
import os
from src.load.load_images import load_image


back_tile_group = pygame.sprite.Group()
front_tile_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

TILE_WIDTH, TILE_HEIGHT = 16, 32


def init_image():
    tile_images = {
        'grass_0': load_image('tiles/grass/grass0.png'),
        'grass_1': load_image('tiles/grass/grass1.png'),
        'grass_2': load_image('tiles/grass/grass2.png'),
        'grass_3': load_image('tiles/grass/grass3.png'),
        'tree_0': load_image('tiles/tree.png'),
        'water_0': load_image('tiles/water/empty_water.png'),
        'water_1': load_image('tiles/water/back_filled_water.png'),
        'water_2': load_image('tiles/water/front_filled_water.png'),
        'tray_0': load_image('tiles/tray/empty_tray.png'),
        'tray_1': load_image('tiles/tray/back_filled_tray.png'),
        'tray_2': load_image('tiles/tray/front_filled_tray.png'),
        'stone_0': load_image('tiles/stone.png'),
        'fence_0': load_image('tiles/fence.png'),
        "path_0": load_image('tiles/path.png'),
        "spawner_0": load_image('tiles/spawner.png')
    }
    return tile_images


class BaseObject(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.orig_image = image
        self.pos_x, self.pos_y = pos_x, pos_y
        self.default_x = self.default_y = self.size_map = 0
        self.orig_size = image.get_size()
        width_rect = self.orig_size[0] * self.pos_x + self.default_x
        height_rect = self.orig_size[0] * self.pos_y + self.default_y
        self.rect = self.image.get_rect().move(width_rect, height_rect)

    def set_default_value(self, def_x, def_y, size):
        self.default_x = def_x
        self.default_y = def_y
        self.size_map = size

    def update(self, vx, vy):
        self.default_x += vx
        self.default_y += vy

    def check(self, horizontal_borders, vertical_borders):
        col_h = []
        for h in horizontal_borders:
            col_h.append(self.image.get_rect().move(self.image.get_rect()[2] * self.pos_x + self.default_x,
                                                    self.image.get_rect()[3] * self.pos_y + self.default_y).colliderect(h.rect))
        col_v = []
        for v in vertical_borders:
            col_v.append(self.image.get_rect().move(self.image.get_rect()[2] * self.pos_x + self.default_x,
                                                    self.image.get_rect()[3] * self.pos_y + self.default_y).colliderect(v.rect))
        return col_h, col_v
        # if pygame.sprite.spritecollideany(self, horizontal_borders):
        #     new_vy = -vy
        # if pygame.sprite.spritecollideany(self, vertical_borders):
        #     new_vx = -vx
        # return new_vx, new_vy

    def draw(self, screen):
        width_rect = self.orig_size[0] * self.pos_x + self.default_x
        height_rect = self.orig_size[0] * self.pos_y + self.default_y
        self.rect = self.image.get_rect().move(width_rect, height_rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def change_size(self, scale):
        new_size = [int(self.orig_size[0] * scale), int(self.orig_size[1] * scale)]

        width_rect = new_size[0] * self.pos_x + self.default_x
        height_rect = new_size[1] * self.pos_y + self.default_y
        self.image = pygame.transform.scale(self.orig_image, new_size)
        self.rect = self.image.get_rect().move(width_rect, height_rect)


class BaseTile(BaseObject):
    def __init__(self, tile_type, pos_x, pos_y, tile_images):
        self.image = tile_images[f"{tile_type}_0"]
        super().__init__(pos_x, pos_y, self.image, tiles_group, all_sprites)


class GrassTile(BaseObject):
    def __init__(self, tile_type, pos_x, pos_y, pointer, tile_images):
        self.image = tile_images[f"{tile_type}_{pointer}"]
        super().__init__(pos_x, pos_y,self.image, tiles_group, all_sprites)


class BackTile(BaseObject):
    def __init__(self, tile_type, pos_x, pos_y, tile_images):
        self.image = tile_images[f"{tile_type}_1"]
        super().__init__(pos_x, pos_y, self.image, back_tile_group, all_sprites)


class FrontTile(BaseObject):
    def __init__(self, tile_type, pos_x, pos_y, tile_images):
        self.image = tile_images[f"{tile_type}_2"]
        super().__init__(pos_x, pos_y, self.image, front_tile_group, all_sprites)


group_list = [tiles_group, back_tile_group, front_tile_group]