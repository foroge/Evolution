import random

import pygame
import sys
import os
from random import randint, choice
import src.objects.tiles
from src.objects.tiles import BaseTile, FrontTile, BackTile, GrassTile, init_image
import src.objects.cats
from src.objects.cats import create_cat, init_cats
from src.extra_utils import WindowSize


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
    wind = WindowSize()
    w, h = wind.w_marge, wind.h_marge
    cats = ["doctor", "egg", "king", "leaf", "mushroom", "transport", "warrior", "wizard", "sunflower"]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'g':
                block = GrassTile('grass', x, y, w, h, randint(0, 3), tile_images)
            elif level[y][x] == 't':
                block1 = GrassTile('grass', x, y, w, h, randint(0, 3), tile_images)
                block2 = BackTile("tray", x, y, w, h, tile_images)
                cat = create_cat(choice(cats), x, y, w, h, cat_images)
                block3 = FrontTile("tray", x, y, w, h, tile_images)
            elif level[y][x] == 'w':
                block1 = GrassTile('grass', x, y, w, h, randint(0, 3), tile_images)
                block2 = BaseTile("water", x, y, w, h, tile_images)
            elif level[y][x] == 'f':
                block = BaseTile("fence", x, y, w, h, tile_images)
            elif level[y][x] == 's':
                block = GrassTile('grass', x, y, w, h, randint(0, 3), tile_images)
            elif level[y][x] == "T":
                block = BaseTile("tree", x, y, w, h, tile_images)
            elif level[y][x] == "-":
                block = BaseTile("stone", x, y, w, h, tile_images)
            elif level[y][x] == '@':
                block1 = GrassTile('grass', x, y, w, h, randint(0, 3), tile_images)
                block2 = BackTile("tray", x, y, w, h, tile_images)
                king = create_cat("king", x, y, w, h, cat_images)
                block3 = FrontTile("tray", x, y, w, h, tile_images)
    return king, x, y, src.objects.tiles.group_list, src.objects.cats.cats_group, src.objects.tiles.all_sprites
