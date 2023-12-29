import pygame
from ..load.load_images import load_image

cat_image = {
    "doctor": load_image("doctor.png"),
    "egg": load_image("egg.png"),
    "king": load_image("king.png"),
    "leaf": load_image("leaf.png"),
    "mushroom": load_image("mushroom.png"),
    "transport": load_image("transport.png"),
    "warrior": load_image("warrior.png"),
    "wizard": load_image("wizard.png"),
}


class BaseCat(pygame.sprite.Sprite):
    def __init__(self, cat_type, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = cat_image[cat_type]
        self.x = tile_width * pos_x + 15
        self.y = tile_height * pos_y + 5
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.xvel = self.yvel = 0