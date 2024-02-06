import pygame
from load.load_images import load_image
from objects.tiles import BaseObject, all_sprites

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
        self.handled = False

    def check_clicked(self, x):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > x:
            click = pygame.mouse.get_pressed()[0]
            if click and self.rect.collidepoint(mouse_pos):
                if not self.handled:
                    self.handled = True
                    return self
                return None
            else:
                self.handled = False
                return None


class BaseProjectile(BaseObject):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image, projectiles_group, all_sprites)


class Doctor(BaseCat):
    def __init__(self, x, y, cat_images):
        self.cat_type = "doctor"
        super().__init__(x, y, self.cat_type, cat_images)


class Egg(BaseCat):
    def __init__(self, x, y, cat_images):
        self.cat_type = "egg"
        super().__init__(x, y, self.cat_type, cat_images)


class Mushroom(BaseCat):
    class PoisonCloudProjectile(pygame.sprite.Sprite):
        def __init__(self, image, dispenser, pos, damage, poison_damage, poison_cloud_time, poison_time, enemy_group):
            super().__init__(projectiles_group, all_sprites)
            self.dispenser = dispenser
            self.pos = pos
            self.frames = []
            self.cut_sheet(image, 10, 1)
            self.cur_frame = 0
            self.image = self.orig_image = self.frames[self.cur_frame]
            self.orig_size = 48, 48
            self.pos = pos
            self.rect = self.image.get_rect(center=(dispenser.rect[0] + 1 / 2 * self.orig_size[0] * pos[0],
                                                    dispenser.rect[1] + 1 / 2 * self.orig_size[1] * pos[1]))
            self.scale = None
            self.enemy_group = enemy_group
            self.damage = damage

            self.poison_damage = poison_damage
            self.poison_cloud_time = self.poison_cloud_time_rest = poison_cloud_time
            self.poison_time = poison_time

            self.anim_time = self.anim_time_rest = 1

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def go_to_enemy(self):
            self.update_rect_anim()
            self.check_collision()
            if self.poison_cloud_time_rest <= 0:
                self.kill()
            else:
                self.poison_cloud_time_rest -= 1 / fps

        def check_collision(self):
            for enemy in self.enemy_group:
                if enemy.rect.colliderect(self.rect):
                    enemy.poisoned = True
                    enemy.poison_time_rest = self.poison_time
                    enemy.poison_damage = self.poison_damage
                    enemy.hp -= self.damage / fps

        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

        def update_rect_anim(self):
            if self.anim_time_rest <= 0:
                self.cur_frame += 1 if self.cur_frame < len(self.frames) - 1 else -3
                self.orig_image = self.frames[self.cur_frame]
                self.anim_time_rest = self.anim_time
            else:
                self.anim_time_rest -= len(self.frames) / fps
            self.rect = self.image.get_rect(center=(self.dispenser.rect[0] + 1 / 2 * self.dispenser.rect[2] +
                                                    self.dispenser.rect[2] * self.pos[0],
                                                    self.dispenser.rect[1] + 1 / 2 * self.dispenser.rect[3] +
                                                    self.dispenser.rect[3] * self.pos[1]))

        def check(self, horizontal_borders, vertical_borders):
            col_h = []
            for h in horizontal_borders:
                col_h.append(self.image.get_rect().move(self.image.get_rect()[0],
                                                        self.image.get_rect()[1]).colliderect(h.rect))
            col_v = []
            for v in vertical_borders:
                col_v.append(self.image.get_rect().move(self.image.get_rect()[0],
                                                        self.image.get_rect()[1]).colliderect(v.rect))
            return col_h, col_v

        def change_size(self, scale):
            self.scale = scale
            new_size = [int(self.orig_size[0] * scale), int(self.orig_size[1] * scale)]
            self.image = pygame.transform.scale(self.orig_image, new_size)
            self.rect = self.image.get_rect(center=(self.dispenser.rect[0] + 1 / 2 * self.dispenser.rect[2] +
                                                    self.dispenser.rect[2] * self.pos[0],
                                                    self.dispenser.rect[1] + 1 / 2 * self.dispenser.rect[3] +
                                                    self.dispenser.rect[3] * self.pos[1]))

    def __init__(self, x, y, cat_images, projectiles_images):
        self.cat_type = "mushroom"
        super().__init__(x, y, self.cat_type, cat_images)
        self.base_radius = self.radius = 48
        self.cooldown = 8
        self.rest_of_cooldown = 0
        self.projectile_image = projectiles_images["poison"]
        self.waiting = False
        self.damage = 15
        self.poison_damage = 10
        self.poison_time = 2
        self.poison_cloud_time = 5
        self.upgrade_cost = 100

    def try_attack(self, enemy_group):
        self.radius = self.base_radius / 0.8 * self.scale
        if self.rest_of_cooldown <= 0:
            self.attack(enemy_group)
            self.rest_of_cooldown = self.cooldown
        else:
            self.rest_of_cooldown -= 1 / fps

    def attack(self, enemy_group):
        for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            self.PoisonCloudProjectile(self.projectile_image, self,
                                       (i, j), self.damage, self.poison_damage,
                                       self.poison_cloud_time, self.poison_time, enemy_group)

    def upgrade(self):
        self.cooldown = round(0.95 * self.cooldown, 1)
        self.damage = round(1.15 * self.damage)
        self.upgrade_cost = round(1.5 * self.upgrade_cost)
        self.poison_damage = round(1.1 * self.poison_damage)
        self.poison_time = round(1.1 * self.poison_time, 1)
        self.poison_cloud_time = round(1.05 * self.poison_cloud_time, 1)


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
        self.cat_type = "electronic"
        super().__init__(x, y, self.cat_type, cat_images)
        self.base_radius = self.radius = 256
        self.cooldown = 2
        self.rest_of_cooldown = 0
        self.projectile_image = projectiles_images["lightning"]
        self.waiting = False
        self.damage = 25
        self.upgrade_cost = 100

    def try_attack(self, enemy_group):
        self.radius = self.base_radius / 0.8 * self.scale
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

    def upgrade(self):
        self.cooldown = round(0.85 * self.cooldown)
        self.damage = round(1.15 * self.damage)
        self.radius = round(1.15 * self.radius)
        self.base_radius = round(1.15 * self.base_radius)
        self.upgrade_cost = round(1.5 * self.upgrade_cost)


class Warrior(BaseCat):
    def __init__(self, x, y, cat_images):
        self.cat_type = "warrior"
        super().__init__(x, y, self.cat_type, cat_images)


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
        self.cat_type = "wizard"
        super().__init__(x, y, self.cat_type, cat_images)
        self.base_radius = self.radius = 128
        self.cooldown = 1
        self.rest_of_cooldown = 0
        self.projectile_image = projectiles_images["magic"]
        self.waiting = False
        self.damage = 15
        self.upgrade_cost = 50

    def try_attack(self, enemy_group):
        self.radius = self.base_radius / 0.8 * self.scale
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

    def upgrade(self):
        self.cooldown = round(0.85 * self.cooldown)
        self.damage = round(1.15 * self.damage)
        self.base_radius = round(1.15 * self.base_radius)
        self.upgrade_cost = round(1.5 * self.upgrade_cost)


class SunFlower(BaseCat):
    def __init__(self, x, y, cat_images):
        self.cat_type = "sunflower"
        super().__init__(x, y, self.cat_type, cat_images)
        self.counter = 0
        self.time_sleep = 3
        self.coins_get = 25
        self.upgrade_cost = 50

    def get_money(self):
        sleep_button = self.counter // self.time_sleep
        if sleep_button:
            self.counter = 0
            return self.coins_get
        return 0

    def upgrade(self):
        self.time_sleep = round(0.85 * self.time_sleep, 2)
        self.coins_get = round(1.15 * self.coins_get)
        self.upgrade_cost = round(1.5 * self.upgrade_cost)


class WaterCat(BaseCat):
    def __init__(self, x, y, cat_images):
        self.cat_type = "water_cat"
        super().__init__(x, y, self.cat_type, cat_images)


def create_cat(name, x, y, cat_images, projectiles_images=None, hp=None):
    if name == "doctor":
        return Doctor(x, y, cat_images)
    elif name == "egg":
        return Egg(x, y, cat_images)
    elif name == "king":
        from objects.king import King
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
