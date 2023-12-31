import pygame
import sys
import os
from random import randint
from src.objects.tiles import BaseTile, FrontTile, BackTile, GrassTile
from src.objects.cats import create_cat


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        return level_map

    except BaseException:
        print("Файл не найден")
        pygame.quit()
        sys.exit()


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'g':
                block = GrassTile('grass', x, y, randint(0, 4))
            elif level[y][x] == 't':
                block = BaseTile("tray", x, y)
            elif level[y][x] == 'w':
                block = BaseTile("tray", x, y)
            elif level[y][x] == 'f':
                block = BaseTile("fence", x, y)
            elif level[y][x] == 's':
                block = BaseTile("stone", x, y)
            elif level[y][x] == '@':
                cat = create_cat("king", x, y)
                block = BaseTile("stone", x, y)
    return x, y