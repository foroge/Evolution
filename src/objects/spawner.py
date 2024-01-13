import pygame
import random
import time
from threading import Thread
from src.load.load_images import load_image
from src.objects.tiles import FrontTile, all_sprites, init_image
from src.objects.enemies import BaseEnemy, init_enemies_images, enemies_group


fps = 60


class Spawner(FrontTile):
    def __init__(self, pos_x, pos_y):
        super().__init__("spawner", pos_x, pos_y, init_image())
        self.enemies_images = init_enemies_images()
        self.wave = 1
        self.difficulty = 1
        self.time_between_waves = 60
        self.time_before_wave = 0
        self.enemy_patterns = [["zombie"]]

    def check_to_spawn(self, new_wave=False):
        if self.time_before_wave <= 0 or new_wave:
            th = Thread(target=self.spawn_wave, args=(random.choice(self.enemy_patterns),
                        random.randint(max([self.difficulty - 4, 1]), self.difficulty + 4),
                        self.difficulty))
            th.start()

            if random.random() <= 0.8:
                self.difficulty += 1
            self.time_before_wave = self.time_between_waves
        else:
            self.time_before_wave -= 1 / fps

    def spawn_wave(self, enemy_types: list[str], count, difficulty):
        for i in range(count):
            randomizing = random.randint(2, 50) / 10

            speed = round(60 * randomizing) / fps
            hp = round(100 / randomizing * (0.9 + difficulty / 10))
            money = 10 + difficulty * 5
            self.spawn(random.choice(enemy_types), speed, hp, money)
            time.sleep(1)

    def spawn(self, enemy_type, speed, hp, money):
        enemy = BaseEnemy(self.pos_x, self.pos_y, enemy_type, self.enemies_images, speed, hp, money)
        enemy.update(self.default_x, self.default_y)
