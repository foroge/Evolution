import pygame
import os
from src.load.load_images import load_image

back_tile_group = pygame.sprite.Group()
front_tile_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

TILE_WIDTH = TILE_HEIGHT = 32


def init_image():
    tile_images = {
        'grass_0': load_image('tiles/grass/grass0.png'),
        'grass_1': load_image('tiles/grass/grass1.png'),
        'grass_2': load_image('tiles/grass/grass2.png'),
        'grass_3': load_image('tiles/grass/grass3.png'),
        'grass_4': load_image('tiles/grass/grass4.png'),
        'water_0': load_image('tiles/water/empty_water.png'),
        'water_1': load_image('tiles/water/back_filled_water.png'),
        'water_2': load_image('tiles/water/front_filled_water.png'),
        'tray_0': load_image('tiles/tray/empty_tray.png'),
        'tray_1': load_image('tiles/tray/back_filled_tray.png'),
        'tray_2': load_image('tiles/tray/front_filled_tray.png'),
        'stone_0': load_image('tiles/stone.png'),
        'fence_0': load_image('tiles/fence.png'),
        # 'wood_0': load_image('tiles/wood.png')
    }
    return tile_images


class BaseTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_images):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[f"{tile_type}_0"]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        print(pos_x, pos_y)


class GrassTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, pointer, tile_images):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[f"{tile_type}_{pointer}"]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class BackTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_images):
        super().__init__(back_tile_group, all_sprites)
        self.image = tile_images[f"{tile_type}_1"]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class FrontTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_images):
        super().__init__(front_tile_group, all_sprites)
        self.image = tile_images[f"{tile_type}_2"]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 16, TILE_HEIGHT * pos_y + 16)
