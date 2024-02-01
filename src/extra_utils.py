import pygame
import json
import os
import sys
from pathlib import Path

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def kill_all_sprites(sprites):
    for g in sprites:
        for s in g:
            s.kill()


def check_cat_clicked(cat_group, x):
    for cat in cat_group:
        check = cat.check_clicked(x)
        if check:
            return check


def loading_screen(sprite, running, screen):
    clock = pygame.time.Clock()
    fps = 36 / 2.39
    while running[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
        screen.fill((40, 40, 40))
        sprite.update()
        sprite.draw(screen)
        pygame.display.update()
        clock.tick(fps)


def spawn_cat(choosen, tile_type, tray, tile_images, cat_images, projectiles_images, back_tile_group, front_tile_group,
              all_sprites):
    from objects.tiles import BackTile, FrontTile
    from objects.cats import create_cat
    x, y = tray.pos_x, tray.pos_y
    b_tile = BackTile(tile_type, x, y, tile_images, [back_tile_group, all_sprites])
    b_tile.set_default_value(tray.default_x, tray.default_y, tray.size_map)
    cat = create_cat(choosen, x, y, cat_images, projectiles_images)
    cat.set_default_value(tray.default_x, tray.default_y, tray.size_map)
    f_tile = FrontTile(tile_type, x, y, tile_images, [front_tile_group, all_sprites])
    f_tile.set_default_value(tray.default_x, tray.default_y, tray.size_map)
    tray.kill()


def destroy_cat(cat, back, front, tile_images, tiles_group, all_sprites):
    from objects.tiles import TrayTile
    pos_x = cat.pos_x
    pos_y = cat.pos_y
    for j in [back, front]:
        for i in j:
            if i.pos_x == pos_x and i.pos_y == pos_y:
                i.kill()
                break
    tile = TrayTile(pos_x, pos_y, tile_images, [tiles_group, all_sprites])
    tile.set_default_value(cat.default_x, cat.default_y, cat.size_map)
    cat.kill()


def check_cat_placed(tiles_group, choosen, x):
    for tile in tiles_group:
        if type(tile).__name__ == "TrayTile":
            clicked = tile.check_clicked(choosen, x)
            if clicked:
                return tile


def update_card(cards, screen, money=0):
    choosen = None
    for card in cards:
        money -= card.button.update(money)
        chose = card.button_choose.update()
        if chose:
            choosen = chose
    return choosen, money
    # for card in cards:
    #     card.all_draw(screen)


def draw_neer_cursor(screen, image):
    screen.blit(image, image.get_rect(center=pygame.mouse.get_pos()))


def update_rect(groups, screen):
    if type(groups) == list:
        for sprites in groups:
            for sprite in sprites:
                sprite.self_draw(screen)
    else:
        for sprite in groups:
            sprite.self_draw(screen)


def change_size_sprites(sprites, camera):
    scale = camera.scale
    for sprite in sprites:
        sprite.change_size(scale)
    cols = [False, False, False, False]
    for sprite in sprites:
        check = sprite.check(horizontal_borders, vertical_borders)
        if not cols[0] and check[0][0]:
            cols[0] = True
        if not cols[1] and check[0][1]:
            cols[1] = True
        if not cols[2] and check[1][0]:
            cols[2] = True
        if not cols[3] and check[1][1]:
            cols[3] = True
    if not all(cols):
        camera.scale += camera.step
        for sprite in sprites:
            sprite.change_size(camera.scale)


def sprites_move(sprites, vx, vy, hor_borders, ver_borders):
    for sprite in sprites:
        sprite.update(vx, vy)
    check = check_collision(sprites, vx, vy, hor_borders, ver_borders)
    if check[0] or check[1]:
        for sprite in sprites:
            sprite.update(check[0], check[1])


def enem_move(sprites, level_map, camera_scale, king):
    count = 0
    for sprite in sprites:
        count += sprite.move(level_map, camera_scale, king)
    return count


def cats_attack(sprites, enemy_group, fps):
    money = 0
    for sprite in sprites:
        if type(sprite).__name__ == "SunFlower":
            sprite.counter += 1 / fps
            money += sprite.get_money()
        elif type(sprite).__name__ != "King":
            sprite.try_attack(enemy_group)
    return money


def move_projectiles(sprites):
    for sprite in sprites:
        sprite.go_to_enemy()


def check_collision(sprites, vx, vy, horizontal_borders, vertical_borders):
    new_vx = 0
    new_vy = 0
    col_h = [False, False]
    col_v = [False, False]
    for sprite in sprites:
        check = sprite.check(horizontal_borders, vertical_borders)
        if not col_h[0] and check[0][0]:
            col_h[0] = True
        if not col_h[1] and check[0][1]:
            col_h[1] = True
        if not col_v[0] and check[1][0]:
            col_v[0] = True
        if not col_v[1] and check[1][1]:
            col_v[1] = True
    if not all(col_h):
        new_vy = -vy
    if not all(col_v):
        new_vx = -vx
    return new_vx, new_vy


def move(sprites, level_map, camera_scale):
    for sprite in sprites:
        sprite.move(level_map, camera_scale)


def set_def_position(sprites, x, y, size):
    for sprite in sprites:
        sprite.set_default_value(x, y, size)


def create_fon_rect(coord=(0, 0), size=(0, 0), color=(0, 0, 0)):
    image = pygame.Surface(size)
    image.fill(color)
    rect = image.get_rect().move(coord)
    return image, rect


def get_json(filename):
    # sys.argv[0] возвращает путь к выполняемому скрипту
    scr_path = "\\".join(sys.argv[0].split("\\")[:-2])
    path = os.path.join(scr_path, "data", filename)
    with open(path) as file:
        data = json.load(file)
    return data


def set_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2 - 20:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([20, y2 - y1])
            self.image.fill((109, 86, 80))
            self.rect = pygame.Rect(x1, y1, 25, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 20])
            self.image.fill((109, 86, 80))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 25)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.scale = 0.8
        self.step = 0.02
        self.old_scale = 0.8

    def change_scale(self, flag):
        if flag and self.scale <= 1.2:
            self.old_scale = self.scale
            self.scale += self.step
        elif not flag and self.scale > 0.8:
            self.old_scale = self.scale
            self.scale -= self.step


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, color="black"):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((150, 150, 150))
        self.rect = self.image.get_rect().move(x, y)

        self.font = pygame.font.Font(None, 25)
        self.text = text
        self.rendered_text = self.font.render(self.text, True, color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)
        self.handled = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.rendered_text, self.text_rect)
        # screen.blit(self.mini_image, self.mini_image_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if click and self.rect.collidepoint(mouse_pos):
            if not self.handled:
                self.handled = True
                # if self.text == "Upgrade":
                #     print(self.handled, self.text)
                return True
            return False
        else:
            self.handled = False
            return False


class WaveButton(Button):
    def __init__(self, x, y, width, height, text, color="black", time_sleep=0):
        super().__init__(x, y, width, height, text, color)
        self.counter = 0
        self.time_sleep = time_sleep
        self.start = True

    def update(self):
        sleep_button = self.counter // self.time_sleep
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if click and self.rect.collidepoint(mouse_pos):
            if not self.handled and sleep_button or self.start:
                self.handled = True
                self.start = False
                self.counter = 0
                return True
            return False
        else:
            self.handled = False
            return False


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x - self.rect[2] // 2, y - self.rect[3] // 2)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
