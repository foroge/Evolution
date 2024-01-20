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
        "lightning": load_image("projectiles/lightning.png"),
        "poison": load_image("projectiles/poison.png")
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


class Mushroom(BaseCat):
    class PoisonCloudProjectile(BaseProjectile):
        def __init__(self, pos_x, pos_y, image, dispenser, new_pos, damage, poison_damage, poison_cloud_time,
                     poison_time, enemy_group):
            super().__init__(pos_x, pos_y, image)
            self.orig_size = 32, 32
            width_rect = self.orig_size[0] * self.pos_x + self.default_x
            height_rect = self.orig_size[0] * self.pos_y + self.default_y
            self.rect = self.image.get_rect().move(width_rect, height_rect)

            self.enemy_group = enemy_group
            self.damage = damage
            self.speed = 64
            x1, y1 = dispenser.rect.center
            self.x2, self.y2 = new_pos[0], new_pos[1]

            self.total_distance = ((((self.x2 + 0.75) * self.orig_size[0] + self.default_x) - x1) ** 2 +
                                   (((self.y2 + 0.75) * self.orig_size[1] + self.default_y) - y1) ** 2) ** 0.5
            self.y_angle = (y1 - ((self.y2 + 0.75) * self.orig_size[1] + self.default_y)) / self.total_distance
            self.x_angle = (x1 - ((self.x2 + 0.75) * self.orig_size[0] + self.default_x)) / self.total_distance
            self.stop = False
            self.poison_damage = poison_damage
            self.poison_cloud_time = self.poison_cloud_time_rest = poison_cloud_time
            self.poison_time = poison_time

        def go_to_enemy(self):
            self.check_collision()
            if not self.stop:
                self.move_x += self.x_angle * self.speed / fps
                self.move_y += self.y_angle * self.speed / fps
            else:
                if self.poison_cloud_time_rest <= 0:
                    self.kill()
                else:
                    self.poison_cloud_time_rest -= 1 / fps

        def check_collision(self):
            if (self.rect.center[0] == ((self.x2 + 0.75) * self.orig_size[0] + self.default_x)
                    and self.rect.center[1] == ((self.y2 + 0.75) * self.orig_size[1] + self.default_y)):
                self.stop = True
            for enemy in self.enemy_group:
                if enemy.rect.colliderect(self.rect):
                    enemy.poisoned = True
                    enemy.poison_time_rest = self.poison_time
                    enemy.poison_damage = self.poison_damage
                    enemy.hp -= 0.5

        def draw(self, screen):
            size = self.rect[2:]
            width_rect = size[0] * self.pos_x + self.default_x + self.move_x
            height_rect = size[0] * self.pos_y + self.default_y + self.move_y
            self.rect = self.image.get_rect().move(width_rect, height_rect)
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def __init__(self, x, y, cat_images, projectiles_images):
        cat_type = "mushroom"
        super().__init__(x, y, cat_type, cat_images)
        self.radius = 24
        self.cooldown = 5
        self.rest_of_cooldown = 0
        self.projectile_image = projectiles_images["poison"]
        self.waiting = False
        self.damage = 15
        self.poison_damage = 50
        self.poison_time = 2
        self.poison_cloud_time = 2

    def try_attack(self, enemy_group):
        if self.rest_of_cooldown <= 0:
            self.attack(enemy_group)
            self.rest_of_cooldown = self.cooldown
        else:
            self.rest_of_cooldown -= 1 / fps

    def attack(self, enemy_group):
        for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            projectile = self.PoisonCloudProjectile(self.pos_x, self.pos_y, self.projectile_image, self,
                                                    (self.pos_x + i, self.pos_y + j), self.damage, self.poison_damage,
                                                    self.poison_cloud_time, self.poison_time, enemy_group)
            projectile.default_x = self.default_x
            projectile.default_y = self.default_y


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
            for sprite in self.enemy_group:
                if sprite.rect.colliderect(pygame.rect.Rect(self.rect[0] - 16, self.rect[1] - 16, 64, 64)):
                    sprite.hp -= self.damage
            self.kill()

    def __init__(self, x, y, cat_images, projectiles_images):
        cat_type = "electronic"
        super().__init__(x, y, cat_type, cat_images)
        self.radius = 256
        self.cooldown = 2
        self.rest_of_cooldown = 0
        self.projectile_image = projectiles_images["lightning"]
        self.waiting = False
        self.damage = 25

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


def create_cat(name, x, y, cat_images, projectiles_images=None, hp=None):
    if name == "doctor":
        return Doctor(x, y, cat_images)
    elif name == "egg":
        return Egg(x, y, cat_images)
    elif name == "king":
        from src.objects.king import King
        return King(x, y, cat_images, hp)
    elif name == "mushroom":
        return Mushroom(x, y, cat_images, projectiles_images)
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
