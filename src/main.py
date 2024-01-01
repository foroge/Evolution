import pygame
import os
import sys
from load.load_images import load_image
from load.load_levels import generate_level, load_level
import objects.cats as obj_cats
from objects.cats import init_cats
import objects.tiles as obj_tiles
from objects.tiles import init_image


pygame.init()

screen_info = pygame.display.Info()
width_full_scr = screen_info.current_w
height_full_scr = screen_info.current_h
screen = pygame.display.set_mode((width_full_scr, height_full_scr - 60))

king, x, y = generate_level(load_level("map1.csv"))

enemies_group = pygame.sprite.Group()   # нужно будет перенести в проект с врагами
ammunition_group = pygame.sprite.Group()  # аналогично


screen.fill((255, 255, 255))
pygame.display.set_caption("Feline Fortress")
running = True
fps = 60
clock = pygame.time.Clock()
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # all_sprites.draw(screen)
    obj_tiles.tiles_group.draw(screen)
    obj_tiles.back_tile_group.draw(screen)
    obj_cats.cats_group.draw(screen)
    obj_tiles.front_tile_group.draw(screen)
    pygame.display.update()
    clock.tick(fps)