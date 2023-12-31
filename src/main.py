import pygame
import os
import sys
from load.load_images import load_image
from load.load_levels import generate_level, load_level


pygame.init()
width_full_scr, height_full_scr = pygame.display.get_surface().get_size()
screen = pygame.display.set_mode((width_full_scr, height_full_scr - 60))

map_load = generate_level(load_level("map1.csv"))

enemies_group = pygame.sprite.Group()   # нужно будет перенести в проект с врагами
ammunition_group = pygame.sprite.Group()  # аналогично


screen.fill((255, 255, 255))
pygame.display.set_caption("Feline Fortress")
running = True
fps = 60

while running:
    left = right = up = down = False
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    pygame.display.update()
    clock.tick(fps)