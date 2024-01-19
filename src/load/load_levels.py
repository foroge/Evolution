import random
import json

import pygame
import sys
import os
from random import randint, choice
import src.objects.tiles
from src.objects.tiles import BaseTile, FrontTile, BackTile, GrassTile, TrayTile, init_image
import src.objects.cats
from src.objects.cats import create_cat, init_cats, init_projectiles
from src.objects.spawner import Spawner
from src.extra_utils import get_json


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
                block = GrassTile('grass', x, y, randint(0, 3), tile_images)
            elif level[y][x] == 'T':
                block1 = GrassTile('grass', x, y, randint(0, 3), tile_images)
                block2 = TrayTile(x, y, tile_images)
            elif level[y][x] == 'w':
                block1 = GrassTile('grass', x, y, randint(0, 3), tile_images)
                block2 = BaseTile("water", x, y, tile_images)
            elif level[y][x] == 'F':
                block = BaseTile("fence", x, y, tile_images)
            elif level[y][x] == 'S':
                block = BaseTile("stone", x, y, tile_images)
            elif level[y][x] == "t":
                block = BaseTile("tree", x, y, tile_images)
            elif level[y][x] == "-":
                block = BaseTile("path", x, y, tile_images)
            elif level[y][x] == "#":
                block1 = BaseTile("path", x, y, tile_images)
                spawner = Spawner(x, y)
            elif level[y][x] == '@':
                block1 = BaseTile("path", x, y, tile_images)
                block2 = BackTile("tray", x, y, tile_images)
                king = create_cat("king", x, y, cat_images, hp=get_json("../data/characteristics.json")["king_hp"])
                block3 = FrontTile("tray", x, y, tile_images)
    return king, spawner, x, y, src.objects.tiles.group_list, src.objects.cats.cats_group, src.objects.tiles.all_sprites
