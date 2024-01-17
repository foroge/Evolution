import pygame
import os
import sys

from load.load_images import load_image
from load.load_levels import generate_level, load_level

import objects.cats as obj_cats
import objects.tiles as obj_tiles
import objects.enemies as obj_enemies

from objects.cats import init_cats, init_projectiles, create_cat, cats_group, projectiles_group
from objects.enemies import init_enemies_images, BaseEnemy, enemies_group
from objects.tiles import init_image

from src.extra_utils import Camera, Button, change_size_sprites, Border, enem_move, sprites_move, set_def_position, \
    check_collision, move_projectiles, cats_attack
import src.extra_utils as extra

from src.tests.create_map import start_creating


pygame.init()
pygame.font.init()

info = pygame.display.Info()
full_w = info.current_w
full_h = info.current_h
screen = pygame.display.set_mode((full_w, full_h))

col_cell = 32

level_map = start_creating(col_cell).copy()
king, spawner, x, y, sprites, cats, all_sprites = generate_level(level_map)
sprites.insert(-1, cats)
sprites.insert(-1, cats_group)
lose_image = load_image("../data/other_images/lose.png")
lose_image = pygame.transform.scale(lose_image, (lose_image.get_rect()[2] * 3, lose_image.get_rect()[3] * 3))
# sprites.append(projectiles_group)

# sprites[-1], sprites[-2] = sprites[-2], sprites[-1]
# enemies_group = pygame.sprite.Group()   # нужно будет перенести в проект с врагами # Перенес
# ammunition_group = pygame.sprite.Group()  # аналогично


screen.fill((255, 255, 255))
pygame.display.set_caption("Feline Fortress")

size_map = full_h - 60
x, y = full_w - size_map - 50, 10

camera = Camera()
next_wave_btn = Button(550, 80, 90, 40, "Next wave", "white")

border1 = Border(x, y, x + 20, y + size_map + 20)
border2 = Border(x + size_map + 15, y, x + size_map + 35, y + size_map + 20)
border3 = Border(x, y, x + size_map + 20, y + 20)
border4 = Border(x, y + size_map + 15, x + size_map + 35, y + size_map + 40)
ver_borders, hor_borders = extra.vertical_borders, extra.horizontal_borders

# Все перениести по другим файлам
# BaseEnemy(spawner.pos_x, spawner.pos_y, "zombie", init_enemies_images(), 60 / camera.scale)
cats_images = init_cats()
projectiles_images = init_projectiles()
# mushroom = create_cat("mushroom", 15, 15, cats_images, projectiles_images)
wizard = create_cat("wizard", 16, 16, cats_images, projectiles_images)
# elctro = create_cat("electronic", 17, 17, cats_images, projectiles_images)
# ===============================

# enemies_group = obj_enemies.enemies_group
all_sprites.add(enemies_group)
all_sprites.add(cats_group)
all_sprites.add(projectiles_group)

sprites_move(all_sprites, x + 20, y + 20, hor_borders, ver_borders)
set_def_position(all_sprites, x + 20, y + 20, size_map)
running = True
running_lose = False
fps = 60
clock = pygame.time.Clock()
speed = 15 / (2 - camera.scale)

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False

while running:
    from src.objects.enemies import enemies_group
    all_sprites.add(enemies_group)

    camera.dx = camera.dy = 0
    screen.fill((255, 255, 255))
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            camera.change_scale(True)
            speed = 15 / (2 - camera.scale)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            camera.change_scale(False)
            speed = 15 / (2 - camera.scale)
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

    enem_move(enemies_group, level_map, camera.scale, king)
    cats_attack(cats_group, enemies_group)
    move_projectiles(projectiles_group)
    spawner.check_to_spawn(new_wave=next_wave_btn.update())

    king.hp_bar.update(king.hp / king.max_hp)
    king.hp_bar.update_wave_text(spawner.wave)
    king.hp_bar.update_time_before_wave(round(spawner.time_before_wave))

    if king.hp == 0:
        running = False
        running_lose = True

    for i in sprites:
        i.draw(screen)
    enemies_group.draw(screen)
    spawner.draw(screen)
    projectiles_group.draw(screen)

    king.hp_bar.draw_health_bar()
    screen.blit(king.hp_bar.image, king.hp_bar.rect)
    screen.blit(king.hp_bar.text_hp_string_rendered, king.hp_bar.text_hp_rect)
    screen.blit(king.hp_bar.text_wave_string_rendered, king.hp_bar.text_wave_rect)
    screen.blit(king.hp_bar.text_time_before_wave_string_rendered, king.hp_bar.text_time_before_wave_rect)

    ver_borders.draw(screen)
    hor_borders.draw(screen)
    next_wave_btn.draw(screen)

    pygame.display.update()
    clock.tick(fps)

while running_lose:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_lose = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running_lose = False
    screen.fill("gray")
    screen.blit(lose_image, lose_image.get_rect(center=screen.get_rect().center))
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
