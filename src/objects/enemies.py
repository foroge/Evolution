import pygame
import random
from src.load.load_images import load_image
from src.objects.tiles import BaseObject, all_sprites

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
    def __init__(self, pos_x, pos_y, enemy_type, enemy_images, speed, hp=100):
        self.enemy_images = enemy_images
        self.enemy_type = enemy_type
        self.image = self.enemy_images[enemy_type]["side"]
        super().__init__(0, 0, self.image, enemies_group, all_sprites)

        self.direction = 0, -1
        self.global_x, self.global_y = self.orig_size[0] * pos_y, self.orig_size[1] * pos_x
        self.margin_x = self.margin_y = 0
        self.passed_cells = set()
        self.once_of_passed_cells = set()
        self.speed = self.standard_speed = speed
        self.hp = hp

    def check_neighbours(self, level_map, now_coords, get_count=False):
        for k in ["@", "-"]:
            neighbours = []
            for i, j in [self.direction, (-self.direction[1], self.direction[0]), (
                    -self.direction[0], -self.direction[1]), (self.direction[1], -self.direction[0])]:
                try:
                    if ((level_map[now_coords[0] + i][now_coords[1] + j] == k)
                            and (now_coords[0] + i, now_coords[1] + j) not in self.passed_cells):
                        neighbours.append((i, j))
                except IndexError:
                    ...
            if not get_count:
                if len(neighbours) == 2:
                    return random.choice(neighbours)
                if len(neighbours) != 0:
                    return neighbours[0]
            elif k == "-":
                return len(neighbours)

    def go(self):
        self.global_x += self.direction[0] * self.speed / fps
        self.global_y += self.direction[1] * self.speed / fps
        # self.rect = self.rect.move(0, 0)
        self.rect = self.rect.move(self.global_y, self.global_x)

    def change_side_image(self, image_type, mirrored=False):
        try:
            image = self.enemy_images[self.enemy_type][image_type]
            if mirrored:
                image = pygame.transform.flip(image, True, False)
            self.image = image
            self.orig_image = image
            self.orig_size = image.get_size()
            # self.rect = self.image.get_rect().move(0, 0)
            self.rect = self.image.get_rect().move(self.global_y, self.global_x)
        except KeyError:
            ...

    def update(self, level_map, camera_scale):
        self.speed = camera_scale * self.standard_speed
        # print(self.global_x, self.global_y, self.rect[0], self.rect[1])
        now_coords = (int((self.global_x - self.margin_x) // self.orig_size[0]),
                      int((self.global_y - self.margin_y) // self.orig_size[1]))
        print(now_coords)
        print(self.global_y, self.global_x)

        if now_coords not in self.passed_cells:
            if now_coords in self.once_of_passed_cells or self.check_neighbours(level_map, now_coords, True) != 3:
                self.passed_cells.add(now_coords)
            else:
                self.once_of_passed_cells.add(now_coords)
        direction = self.check_neighbours(level_map, now_coords)
        if self.direction != direction:
            self.direction = direction
            if self.direction == (-1, 0):
                self.change_side_image("side")
            elif self.direction == (1, 0):
                self.change_side_image("side", True)
            elif self.direction == (0, -1):
                self.change_side_image("back")
            elif self.direction == (0, 1):
                self.change_side_image("front")
        if self.hp == 0:
            self.kill()
        else:
            if level_map[now_coords[0]][now_coords[1]] == "@":
                # Еще нужно нанести королю урон, но у нас такого нет еще
                self.kill()
            else:
                self.go()
                # print(now_coords)
                # print(int((self.rect[0] - self.margin_x) // self.orig_size[0]),
                #       int((self.rect[1] - self.margin_y) // self.orig_size[1]))