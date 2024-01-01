import pygame
import os
import sys

from load.load_images import load_image
from load.load_levels import generate_level, load_level
import objects.cats as obj_cats
from objects.cats import init_cats
import objects.tiles as obj_tiles
from objects.tiles import init_image
from src.extra_utils import WindowSize, Camera, change_size_sprites


pygame.init()

wind = WindowSize()

screen = pygame.display.set_mode((wind.size_w, wind.size_h))

king, x, y, sprites, cats, all_sprites = generate_level(load_level("map1.csv"))
sprites.append(cats)

sprites[-1], sprites[-2] = sprites[-2], sprites[-1]
enemies_group = pygame.sprite.Group()   # нужно будет перенести в проект с врагами
ammunition_group = pygame.sprite.Group()  # аналогично

screen.fill((255, 255, 255))
pygame.display.set_caption("Feline Fortress")

camera = Camera()

running = True
fps = 60
clock = pygame.time.Clock()
speed = 10
while running:
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
    change_size_sprites(all_sprites, camera.scale)
    for i in sprites:
        i.draw(screen)
    pygame.display.update()
    clock.tick(fps)