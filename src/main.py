import pygame
import os
import sys

from load.load_images import load_image
from load.load_levels import generate_level, load_level
import objects.cats as obj_cats
from objects.cats import init_cats
import objects.tiles as obj_tiles
from objects.tiles import init_image
from src.extra_utils import Camera, change_size_sprites, Border, sptires_move, set_def_position, check_collision
import src.extra_utils as extra
from src.tests.create_map import create_map


pygame.init()

info = pygame.display.Info()
full_w = info.current_w
full_h = info.current_h
screen = pygame.display.set_mode((full_w, full_h))

col_cell = 32

king, x, y, sprites, cats, all_sprites = generate_level(create_map(col_cell))
sprites.append(cats)

sprites[-1], sprites[-2] = sprites[-2], sprites[-1]
enemies_group = pygame.sprite.Group()   # нужно будет перенести в проект с врагами
ammunition_group = pygame.sprite.Group()  # аналогично


screen.fill((255, 255, 255))
pygame.display.set_caption("Feline Fortress")

size_map = full_h - 60
x, y = full_w - size_map - 50, 10

camera = Camera()

border1 = Border(x, y, x + 20, y + size_map + 20)
border2 = Border(x + size_map + 15, y, x + size_map + 35, y + size_map + 20)
border3 = Border(x, y, x + size_map + 20, y + 20)
border4 = Border(x, y + size_map + 15, x + size_map + 35, y + size_map + 40)
ver_borders, hor_borders = extra.vertical_borders, extra.horizontal_borders
set_def_position(all_sprites, x + 30, y + 30, size_map)
running = True
fps = 60
clock = pygame.time.Clock()
speed = 10
while running:
    camera.dx = camera.dy = 0
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_a:
                camera.dx -= speed
            if event.key == pygame.K_d:
                camera.dx += speed
            if event.key == pygame.K_w:
                camera.dy -= speed
            if event.key == pygame.K_s:
                camera.dy += speed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            camera.change_scale(True)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            camera.change_scale(False)
    sptires_move(all_sprites, camera.dx, camera.dy, hor_borders, ver_borders)
    change_size_sprites(all_sprites, camera.scale)
    ver_borders.draw(screen)
    hor_borders.draw(screen)
    for i in sprites:
        i.draw(screen)
    pygame.display.update()
    clock.tick(fps)