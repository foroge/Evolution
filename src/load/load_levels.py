import random
import json

import pygame
import sys
import os
from random import randint, choice
import objects.tiles
from objects.tiles import BaseTile, FrontTile, BackTile, GrassTile, TrayTile, init_image
import objects.cats
from objects.cats import create_cat, init_cats, init_projectiles
from objects.spawner import Spawner
from extra_utils import get_json


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
    spawner = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'g':
                GrassTile('grass', x, y, randint(0, 3), tile_images)
            elif level[y][x] == 'T':
                GrassTile('grass', x, y, randint(0, 3), tile_images)
                TrayTile(x, y, tile_images)
            elif level[y][x] == 'w':
                GrassTile('grass', x, y, randint(0, 3), tile_images)
                BaseTile("water", x, y, tile_images)
            elif level[y][x] == 'F':
                BaseTile("fence", x, y, tile_images)
            elif level[y][x] == 'S':
                BaseTile("stone", x, y, tile_images)
            elif level[y][x] == "t":
                BaseTile("tree", x, y, tile_images)
            elif level[y][x] == "-":
                BaseTile("path", x, y, tile_images)
            elif level[y][x] == "#":
                BaseTile("path", x, y, tile_images)
                spawner = Spawner(x, y)
            elif level[y][x] == '@':
                BaseTile("path", x, y, tile_images)
                BackTile("tray", x, y, tile_images)
                king = create_cat("king", x, y, cat_images, hp=get_json("characteristics.json")[0]["king_hp"])
                FrontTile("tray", x, y, tile_images)
    return king, spawner, x, y, objects.tiles.group_list.copy(), objects.cats.cats_group, objects.tiles.all_sprites
