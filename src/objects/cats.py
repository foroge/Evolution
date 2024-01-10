import pygame
from src.load.load_images import load_image
from src.objects.tiles import BaseObject, all_sprites

cats_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()
fps = 60


def init_cats():
    cat_image = {
        "doctor": load_image("cats/doctor.png"),
        "egg": load_image("cats/egg.png"),
        "king": load_image("cats/king.png"),
        "mushroom": load_image("cats/mushroom.png"),
        "electronic": load_image("cats/electronic.png"),
        "warrior": load_image("cats/warrior.png"),
        "wizard": load_image("cats/wizard.png"),
        "sunflower": load_image("cats/sunflower.png"),
        "water_cat": load_image("cats/water_cat.png")
    }
    return cat_image


def init_projectiles():
    images = {
        "magic": load_image("projectiles/magic.png"),
        "lightning": load_image("projectiles/lightning.png")
    }
    return images


class BaseCat(BaseObject):
    def __init__(self, pos_x, pos_y, cat_type, cat_images):
        self.image = cat_images[cat_type]
        super().__init__(pos_x, pos_y, self.image, cats_group, all_sprites)


class BaseProjectile(BaseObject):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image, projectiles_group, all_sprites)


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


class Mushroom(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "mushroom"
        super().__init__(x, y, cat_type, cat_images)


class Electronic(BaseCat):
    class LightningProjectile(BaseProjectile):
        def __init__(self, pos_x, pos_y, image, enemy_group, damage):
            super().__init__(pos_x, pos_y, image)
            self.damage = damage
            self.enemy_group = enemy_group
            self.time = 0.5

        def go_to_enemy(self):
            if self.time <= 0:
                self.check_collision()
            else:
                self.time -= 1 / fps

        def check_collision(self):
            count = 0
            for sprite in self.enemy_group:
                if sprite.rect.colliderect(pygame.rect.Rect(self.rect[0] - 16, self.rect[1] - 16, 64, 64)):
                    sprite.hp -= self.damage
                    print(sprite.hp)
                    count += 1
            self.kill()

    def __init__(self, x, y, cat_images, projectiles_images):
        cat_type = "electronic"
        super().__init__(x, y, cat_type, cat_images)
        self.radius = 256
        self.cooldown = 2
        self.rest_of_cooldown = 0
        self.projectile_image = projectiles_images["lightning"]
        self.waiting = False
        self.damage = 50

    def try_attack(self, enemy_group):
        if self.rest_of_cooldown <= 0:
            self.attack(enemy_group)
            if not self.waiting:
                self.rest_of_cooldown = self.cooldown
        else:
            self.rest_of_cooldown -= 1 / fps

    def attack(self, enemy_group):
        valid_enemies = []
        for enemy in enemy_group:
            x1, y1 = self.rect.center
            x2, y2 = enemy.rect.center
            if ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 <= self.radius:
                valid_enemies.append((enemy, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5))
        if valid_enemies:
            self.waiting = False
            enemy = min(valid_enemies, key=lambda x: x[1])[0]
            projectile = self.LightningProjectile(enemy.pos_x, enemy.pos_y,
                                                  self.projectile_image, enemy_group, self.damage)
            projectile.default_x = self.default_x
            projectile.default_y = self.default_y
        else:
            self.waiting = True


class Warrior(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "warrior"
        super().__init__(x, y, cat_type, cat_images)


class Wizard(BaseCat):
    class MagicProjectile(BaseProjectile):
        def __init__(self, pos_x, pos_y, image, dispenser, enemy, enemy_group, damage):
            super().__init__(pos_x, pos_y, image)
            self.damage = damage
            self.enemy = enemy
            self.enemy_group = enemy_group
            self.speed = 512
            x1, y1 = dispenser.rect.center
            x2, y2 = enemy.rect.center
            self.total_distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            self.y_angle = (y1 - y2) / self.total_distance
            self.x_angle = (x1 - x2) / self.total_distance
            # (self.newpos[0] - self.pos[0]) ** 2 + (self.newpos[1] - self.pos[1]) ** 2 = (self.speed / fps) ** 2

        def go_to_enemy(self):
            self.check_collision()
            self.move_x -= self.x_angle * self.speed / fps
            self.move_y -= self.y_angle * self.speed / fps

        def check_collision(self):
            count = 0
            for sprite in self.enemy_group:
                if sprite.rect.colliderect(pygame.rect.Rect(self.rect.center[0] - 8, self.rect.center[1] - 8, 16, 16)):
                    sprite.hp -= self.damage
                    count += 1
            if count > 0:
                self.kill()

    def __init__(self, x, y, cat_images, projectiles_images):
        cat_type = "wizard"
        super().__init__(x, y, cat_type, cat_images)
        self.radius = 128
        self.cooldown = 1
        self.rest_of_cooldown = 0
        self.projectile_image = projectiles_images["magic"]
        self.waiting = False
        self.damage = 15

    def try_attack(self, enemy_group):
        if self.rest_of_cooldown <= 0:
            self.attack(enemy_group)
            if not self.waiting:
                self.rest_of_cooldown = self.cooldown
        else:
            self.rest_of_cooldown -= 1 / fps

    def attack(self, enemy_group):
        valid_enemies = []
        for enemy in enemy_group:
            x1, y1 = self.rect.center
            x2, y2 = enemy.rect.center
            if ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 <= self.radius:
                valid_enemies.append((enemy, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5))
        if valid_enemies:
            self.waiting = False
            enemy = min(valid_enemies, key=lambda x: x[1])[0]
            projectile = self.MagicProjectile(self.pos_x, self.pos_y,
                                              self.projectile_image, self, enemy, enemy_group, self.damage)
            projectile.default_x = self.default_x
            projectile.default_y = self.default_y
        else:
            self.waiting = True


class SunFlower(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "sunflower"
        super().__init__(x, y, cat_type, cat_images)


class WaterCat(BaseCat):
    def __init__(self, x, y, cat_images):
        cat_type = "water_cat"
        super().__init__(x, y, cat_type, cat_images)


def create_cat(name, x, y, cat_images, projectiles_images=None):
    if name == "doctor":
        return Doctor(x, y, cat_images)
    elif name == "egg":
        return Egg(x, y, cat_images)
    elif name == "king":
        return King(x, y, cat_images)
    elif name == "mushroom":
        return Mushroom(x, y, cat_images)
    elif name == "electronic":
        return Electronic(x, y, cat_images, projectiles_images)
    elif name == "warrior":
        return Warrior(x, y, cat_images)
    elif name == "wizard":
        return Wizard(x, y, cat_images, projectiles_images)
    elif name == "sunflower":
        return SunFlower(x, y, cat_images)
    elif name == "water_cat":
        return WaterCat(x, y, cat_images)
