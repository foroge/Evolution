import pygame
from src.load.load_images import load_image
from src.objects.tiles import BaseObject, all_sprites

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
        "sunflower": load_image("cats/sunflower.png")
    }
    return cat_image


class BaseCat(BaseObject):
    def __init__(self, pos_x, pos_y, cat_type, cat_images):
        self.image = cat_images[cat_type]
        super().__init__(pos_x, pos_y, self.image, cats_group, all_sprites)


class Doctor(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "doctor"
        super().__init__(x, y, cat_type, cat_images)


class Egg(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "egg"
        super().__init__(x, y, cat_type, cat_images)


class King(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "king"
        super().__init__(x, y, cat_type, cat_images)


class Leaf(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "leaf"
        super().__init__(x, y, cat_type, cat_images)


class Mushroom(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "mushroom"
        super().__init__(x, y, cat_type, cat_images)


class Transport(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "transport"
        super().__init__(x, y, cat_type, cat_images)


class Warrior(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "warrior"
        super().__init__(x, y, cat_type, cat_images)


class Wizard(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "wizard"
        super().__init__(x, y, cat_type, cat_images)


class SunFlower(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "sunflower"
        super().__init__(x, y, cat_type, cat_images)


def create_cat(name, x, y, cat_images):
    if name == "doctor":
        return Doctor(x, y, cat_images)
    elif name == "egg":
        return Egg(x, y, cat_images)
    elif name == "king":
        return King(x, y, cat_images)
    elif name == "leaf":
        return Leaf(x, y, cat_images)
    elif name == "mushroom":
        return Mushroom(x, y, cat_images)
    elif name == "transport":
        return Transport(x, y, cat_images)
    elif name == "warrior":
        return Warrior(x, y, cat_images)
    elif name == "wizard":
        return Wizard(x, y, cat_images)
    elif name == "sunflower":
        return SunFlower(x, y, cat_images)