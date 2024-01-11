import pygame
import os
import sys

from load.load_images import load_image
from load.load_levels import generate_level, load_level
import objects.cats as obj_cats
from objects.cats import init_cats
import objects.enemies
from objects.enemies import init_enemies_images, BaseEnemy
import objects.tiles as obj_tiles
from objects.tiles import init_image
from src.extra_utils import Camera, change_size_sprites, Border, update_rect, enem_move, sprites_move, set_def_position, check_collision
import src.extra_utils as extra
from src.tests.create_map import create_map


pygame.init()

info = pygame.display.Info()
full_w = info.current_w
full_h = info.current_h
screen = pygame.display.set_mode((full_w, full_h))

col_cell = 32

level_map = create_map(col_cell).copy()
king, spawner, x, y, sprites, cats, all_sprites = generate_level(level_map)
sprites.append(cats)

sprites[-1], sprites[-2] = sprites[-2], sprites[-1]
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

print(spawner.pos_x, spawner.pos_y)
# BaseEnemy(spawner.pos_x, spawner.pos_y, "zombie", init_enemies_images(), 200 / camera.scale)
enemies_group = objects.enemies.enemies_group
all_sprites.add(enemies_group)

sprites_move(all_sprites, x + 20, y + 20, hor_borders, ver_borders)

running = True
fps = 60
clock = pygame.time.Clock()
speed = 15 / (2 - camera.scale)

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False
x_mouse = y_mouse = 0
while running:
    camera.dx = camera.dy = 0
    screen.fill((250, 222, 154))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_a:
                a_pressed = True
            if event.key == pygame.K_d:
                d_pressed = True
            if event.key == pygame.K_w:
                w_pressed = True
            if event.key == pygame.K_s:
                s_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_pressed = False
            if event.key == pygame.K_d:
                d_pressed = False
            if event.key == pygame.K_w:
                w_pressed = False
            if event.key == pygame.K_s:
                s_pressed = False
        if event.type == pygame.MOUSEMOTION:
            x_mouse = event.pos[0]
            y_mouse = event.pos[1]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and x_mouse > x:
            camera.change_scale(True)
            speed = 15 / (2 - camera.scale)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and x_mouse > x:
            camera.change_scale(False)
            speed = 15 / (2 - camera.scale)
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #     BaseEnemy(spawner.pos_x, spawner.pos_y, "zombie", init_enemies_images(), 200 / camera.scale)
        #     enemies_group = objects.enemies.enemies_group
    if a_pressed:
        camera.dx += speed
    if d_pressed:
        camera.dx -= speed
    if w_pressed:
        camera.dy += speed
    if s_pressed:
        camera.dy -= speed

    sprites_move(all_sprites, camera.dx, camera.dy, hor_borders, ver_borders)
    change_size_sprites(all_sprites, camera)

    enem_move(enemies_group, level_map, camera.scale)
    update_rect(sprites, screen)
    update_rect(enemies_group, screen)
    ver_borders.draw(screen)
    hor_borders.draw(screen)

    pygame.display.update()
    clock.tick(fps)
