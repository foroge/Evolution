import pygame
from ..load.load_images import load_image


tile_images = {
    'grass_0': load_image('grass.png'),
    'grass_1': load_image('grass.png'),
    'grass_2': load_image('grass.png'),
    'grass_3': load_image('grass.png'),
    'grass_4': load_image('grass.png'),
    'water_0': load_image('water/empty_water.png'),
    'water_1': load_image('water/back_filled_water.png'),
    'water_2': load_image('water/front_filled_water.png'),
    'tray_0': load_image('tray/empty_tray.png'),
    'tray_1': load_image('tray/back_filled_tray.png'),
    'tray_2': load_image('tray/front_filled_tray.png'),
    'stone': load_image('stone.png'),
    'fence': load_image('fence.png'),
    'wood': load_image('wood.png')
}


class BaseTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class CustomTile(pygame.sprite.Sprite):
    def __init___(self, tile_type, pos_x, pos_y, pointer):
        super()._init__(tiles_group, all_sprites)
        self.image = tile_images[f"{tile_type}_{pointer}"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)