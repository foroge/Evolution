import pygame
import sys
import os
from random import randint
from src.objects.tiles import BaseTile, FrontTile, BackTile, GrassTile, init_image
from src.objects.cats import create_cat, init_cats


def load_level(filename):
    dirname = "/".join(os.path.dirname(__file__).split("\\")[:-2])
    filename = "/".join([dirname, "data", "maps", filename])
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        return level_map

    except BaseException as e:
        print(e)
        print("Файл не найден")
        pygame.quit()
        sys.exit()


def generate_level(level):
    king, x, y = None, None, None
    tile_images = init_image()
    cat_images = init_cats()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'g':
                block = GrassTile('grass', x, y, randint(0, 4), tile_images)
            elif level[y][x] == 't':
                block = BaseTile("tray", x, y, tile_images)
            elif level[y][x] == 'w':
                block = BaseTile("tray", x, y, tile_images)
            elif level[y][x] == 'f':
                block = BaseTile("fence", x, y, tile_images)
            elif level[y][x] == 's':
                block = BaseTile("stone", x, y, tile_images)
            elif level[y][x] == '@':
                block1 = GrassTile('grass', x, y, randint(0, 4), tile_images)
                block2 = BackTile("tray", x, y, tile_images)
                king = create_cat("king", x, y, cat_images)
                block3 = FrontTile("tray", x, y, tile_images)
    return king, x, y