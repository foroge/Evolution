import pygame
import random
from load.load_images import load_image
from objects.tiles import BaseObject, all_sprites

enemies_group = pygame.sprite.Group()
fps = 60


def init_enemies_images():
    enemy_images = {
        "zombie": {"side": load_image("enemies/zombie/side.png"), }
                   # "back": load_image("enemies/zombie/back.png"), # Его нет еще
                   # "front": load_image("enemies/zombie/front.png")}, # Его нет еще
    }
    return enemy_images


class BaseEnemy(BaseObject):
    def __init__(self, pos_x, pos_y, enemy_type, enemy_images, speed, hp, money):
        self.enemy_images = enemy_images
        self.enemy_type = enemy_type
        self.image = self.enemy_images[enemy_type]["side"]
        super().__init__(pos_x, pos_y, self.image, enemies_group, all_sprites)
        self.new_pos_x = self.new_pos_y = 0
        self.spawn_def = (self.default_x, self.default_y)
        self.direction = 0, -1
        self.back = -self.direction[0], -self.direction[1]
        self.passed_cells = set()
        self.speed = self.standard_speed = speed
        self.hp = hp
        self.money = money
        self.poisoned = False
        self.poison_time_rest = 0
        self.poison_damage = 0

    def check_neighbours(self, level_map, now_coords):
        if self.move_x != 0 or self.move_y != 0:
            return self.direction
        possible_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        valid_directions = []

        for direction in possible_directions:
            i, j = direction
            try:
                i2, j2 = int(now_coords[0]) + i, int(now_coords[1]) + j
                if level_map[i2][j2] == "@":
                    return direction
                if level_map[i2][j2] == "-" and ((i2, j2), direction) not in self.passed_cells:
                    valid_directions.append(direction)
            except IndexError:
                pass
        forward_direction = (self.direction[0], self.direction[1])
        if forward_direction in valid_directions:
            return forward_direction
        if valid_directions:
            return random.choice(valid_directions)

    def go(self):
        try:
            size = self.image.get_size()
            self.move_x += round(self.direction[1] * self.speed / fps)
            self.move_y += round(self.direction[0] * self.speed / fps)
            if self.move_x // size[0] == 1 or self.move_y // size[1] == 1:
                self.back = -self.direction[0], -self.direction[1]
            self.pos_x += self.move_x // size[0]
            self.pos_y += self.move_y // size[1]
            self.move_x %= size[0]
            self.move_y %= size[1]
        except ZeroDivisionError:
            ...
        except TypeError:
            self.kill()

    def change_side_image(self, image_type, mirrored=False):
        try:
            image = self.enemy_images[self.enemy_type][image_type]
            if mirrored:
                image = pygame.transform.flip(image, True, False)
            self.image = image
            self.orig_image = image
            self.orig_size = image.get_size()
            self.change_size(self.scale)
        except KeyError:
            ...

    def move(self, level_map, camera_scale, king):
        self.poison_damaging()
        self.speed = camera_scale * self.standard_speed
        now_coords = (int(self.pos_y), int(self.pos_x))
        self.passed_cells.add((now_coords, (-self.direction[0], -self.direction[1])))
        direction = self.check_neighbours(level_map, now_coords)
        if not direction:
            self.direction = self.back
        # print(now_coords)
        if self.direction != direction:
            self.direction = direction
            if self.direction == (-1, 0):
                self.change_side_image("back")
            if self.direction == (1, 0):
                self.change_side_image("front")
            if self.direction == (0, -1):
                self.change_side_image("side")
            if self.direction == (0, 1):
                self.change_side_image("side", True)
        if self.hp <= 0:
            self.kill()
            return self.money
        else:
            if level_map[now_coords[0]][now_coords[1]] == "@":
                king.hp -= 1
                self.kill()
            else:
                self.go()
        return 0

    def poison_damaging(self):
        if self.poisoned:
            if self.poison_time_rest <= 0:
                self.poisoned = False
                self.poison_time_rest = 0
                self.poison_damage = 0
            else:
                self.poison_time_rest -= 1 / fps
                self.hp -= self.poison_damage / fps

