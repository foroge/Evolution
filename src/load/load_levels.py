import pygame
import sys
from ..objects.tiles import BaseTile, CustomTile
from random import randint
from ..objects.cats import create_cat


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
    cats, blocks, x, y = [], [], None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'g':
                if level[y][x] in ["конст список котов"]:
                    block = CustomTile('grass', x, y, randint(0, 4))
                    cat = create_cat(level[y][x])
                    blocks.append(block)
                    cats.append(cat)
                else:
                    block = CustomTile('grass', x, y, randint(0, 4))
                    blocks.append(block)
            elif level[y][x] == 't':
                if level[y][x] in ["конст список котов"]:
                    block1 = CustomTile("tray", x, y, 1)
                    cat = create_cat(level[y][x])
                    block2 = CustomTile("tray", x, y, 2)
                    blocks.append(block1)
                    blocks.append(block2)
                    cats.append(cat)
                else:
                    block = CustomTile("tray", x, y, 0)
                    blocks.append(block)
            elif level[y][x] == 'w':
                if level[y][x] in ["конст список котов"]:
                    block1 = CustomTile("tray", x, y, 1)
                    cat = create_cat(level[y][x])
                    block2 = CustomTile("tray", x, y, 2)
                    blocks.append(block1)
                    blocks.append(block2)
                    cats.append(cat)
                else:
                    block = CustomTile("tray", x, y, 0)
                    blocks.append(block)
            elif level[y][x] == 'f':
                block = BaseTile("fence", x, y)
                cat = create_cat(level[y][x])
                blocks.append(block)
                cats.append(cat)
            elif level[y][x] == 's':
                block = BaseTile("stone", x, y)
                cat = create_cat(level[y][x])
                blocks.append(block)
                cats.append(cat)
    return cats, blocks, x, y