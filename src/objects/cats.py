import pygame
from src.load.load_images import load_image

cats_group = pygame.sprite.Group()


def init_cats():
    cat_image = {
        "doctor": load_image("cats/doctor.png"),
        "egg": load_image("cats/egg.png"),
        "king": load_image("cats/king.png"),
        "leaf": load_image("cats/leaf.png"),
        "mushroom": load_image("cats/mushroom.png"),
        "transport": load_image("cats/transport.png"),
        "warrior": load_image("cats/warrior.png"),
        "wizard": load_image("cats/wizard.png"),
    }
    return cat_image


class BaseCat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, cat_type):
        super().__init__(player_group, all_sprites)
        self.image = cat_image[cat_type]
        self.x = tile_width * pos_x + 15
        self.y = tile_height * pos_y + 5
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.xvel = self.yvel = 0


class Doctor(BaseCat):
    pass


class Egg(BaseCat):
    pass


class King(BaseCat):
    def __init__(self, x, y):
        cat_type = "king"
        super().__init__(x, y, cat_type)


class Leaf(BaseCat):
    pass


class Mushroom(BaseCat):
    pass


class Transport(BaseCat):
    pass


class Warrior(BaseCat):
    pass


class Wizard(BaseCat):
    pass


def create_cat(name, x, y):
    if name == "doctor":
        return Doctor("doctor", x, y)
    elif name == "egg":
        return Egg(x, y)
    elif name == "king":
        return King(x, y)
    elif name == "leaf":
        return Leaf(x, y)
    elif name == "mushroom":
        return Mushroom(x, y)
    elif name == "transport":
        return Transport(x, y)
    elif name == "warrior":
        return Warrior(x, y)
    elif name == "wizard":
        return Wizard(x, y)