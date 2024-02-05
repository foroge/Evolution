import pygame
import os
import sys

from threading import Thread
import time

from load.load_images import load_image
from load.load_levels import generate_level, load_level

import objects.cats as obj_cats
from objects.cats import init_cats
import objects.enemies
from objects.enemies import init_enemies_images, BaseEnemy
import objects.tiles as obj_tiles
import objects.enemies as obj_enemies

from objects.cats import init_cats, init_projectiles, create_cat, cats_group, projectiles_group
from objects.enemies import init_enemies_images, BaseEnemy, enemies_group
from objects.tiles import init_image

from extra_utils import Camera, change_size_sprites, Border, enem_move, sprites_move, set_def_position
from extra_utils import check_collision, move_projectiles, cats_attack, update_rect, update_card, Button
from extra_utils import draw_neer_cursor, check_cat_placed, spawn_cat, get_json, WaveButton, create_fon_rect
from extra_utils import AnimatedSprite, loading_screen, check_cat_clicked, destroy_cat, kill_all_sprites, set_json
import extra_utils as extra

from tests.create_map import start_creating
from load.card_cats import BaseCard

from ui.pause_menu import PauseMenu
from ui.money_counter import MoneyCounter
from ui.cat_upgrade_menu import UpgradeMenu
from ui.statistics_menu import StatisticsMenu
from ui.main_menu import MainMenu

from data_base.data_base import DBViewer


upgrade_menu: UpgradeMenu


def game(screen):
    global upgrade_menu

    info = pygame.display.Info()
    full_w = info.current_w
    full_h = info.current_h

    run_loading_screen = [True]
    loading_screen_sprite = AnimatedSprite(load_image("../data/other_images/chipi_chipi_spritesheet.png"), 6, 6,
                                           full_w // 2, full_h // 2)
    t1 = Thread(target=loading_screen, args=(loading_screen_sprite, run_loading_screen, screen), daemon=True)
    t1.start()

    col_cell = 32

    level_map = start_creating(col_cell).copy()
    king, spawner, x, y, sprites, cats, all_sprites = generate_level(level_map)
    sprites.insert(-1, cats)
    sprites.insert(-1, cats_group)
    lose_image = load_image("../data/other_images/lose.png")
    lose_image = pygame.transform.scale(lose_image, (lose_image.get_rect()[2] * 3, lose_image.get_rect()[3] * 3))
    wave_width = 90
    wave_height = 40
    wave_btn_x = king.hp_bar.rect.left
    wave_btn_y = king.hp_bar.rect.top + king.hp_bar.rect.height + 10
    next_wave_btn = WaveButton(x=wave_btn_x, y=wave_btn_y, width=wave_width, height=wave_height,
                               text="Next wave", color="white", time_sleep=3)

    money_counter_height = 40
    money_counter_width = 50
    money_counter_x = king.hp_bar.rect.right - (money_counter_width / 2)
    money_counter_y = king.hp_bar.rect.top + king.hp_bar.rect.height + 18
    money_counter = MoneyCounter(x=money_counter_x, y=money_counter_y, width=money_counter_width, height=money_counter_height)

    screen.fill((255, 255, 255))
    pygame.display.set_caption("Feline Fortress")

    size_map = full_h - 60
    x, y = full_w - size_map - 50, 10

    camera = Camera()

    border1 = Border(x, y, x + 20, y + size_map + 20)
    border2 = Border(x + size_map + 15, y, x + size_map + 35, y + size_map + 20)
    border3 = Border(x, y, x + size_map + 20, y + 20)
    border4 = Border(x, y + size_map + 15, x + size_map + 35, y + size_map + 40)
    ver_borders, hor_borders = extra.vertical_borders, extra.horizontal_borders

    image1, rect1 = create_fon_rect(size=(x, full_w), color=(250, 222, 154))
    image2, rect2 = create_fon_rect(coord=(x, 0), size=(size_map + 35, 30), color=(250, 222, 154))
    image3, rect3 = create_fon_rect(coord=(x, y + size_map + 35), size=(size_map + 35, 30), color=(250, 222, 154))
    image4, rect4 = create_fon_rect(coord=(x + size_map + 35, 0), size=(x, full_w), color=(250, 222, 154))

    cat_images = init_cats()
    tile_images = init_image()

    projectiles_images = init_projectiles()

    cards = []
    x_card, y_card = -80, 140
    # cat_names = ["doctor", "egg", "mushroom", "electronic", "warrior", "wizard", "sunflower", "water_cat"]
    cat_names = ["wizard", "electronic", "sunflower", "mushroom"]
    for i in cat_names:
        image = cat_images[i]
        x_card += 100
        if x_card + 64 > x:
            x_card = 20
            y_card += 181
        cat_cost = get_json("../data/characteristics.json")[1]["cats_cost"][i]
        card = BaseCard(x=x_card, y=y_card, cost=cat_cost, name_text=i, custom_image=image)
        cards.append(card)

    all_sprites.add(enemies_group)
    all_sprites.add(cats_group)
    all_sprites.add(projectiles_group)

    darken_surface = pygame.Surface((full_w, full_h))
    darken_surface.set_alpha(128)
    darken_surface.fill((0, 0, 0))
    pause_menu = PauseMenu(full_w // 2, full_h // 2)

    sprites_move(all_sprites, x + 20, y + 20, hor_borders, ver_borders)
    set_def_position(all_sprites, x + 20, y + 20, size_map)
    running = True
    running_lose = False
    paused = False
    fps = 60
    clock = pygame.time.Clock()
    speed = 15 / (2 - camera.scale)
    choosen = None
    upgrade_menu_called = None

    w_pressed = False
    a_pressed = False
    s_pressed = False
    d_pressed = False
    x_mouse = y_mouse = 0

    time.sleep(2.39)
    run_loading_screen[0] = False

    all_money = 0
    all_kills = 0

    while running:
        all_sprites.add(enemies_group)

        camera.dx = camera.dy = 0
        screen.fill((75, 105, 47))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill_all_sprites([*sprites, enemies_group, projectiles_group])
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if event.key == pygame.K_a:
                    a_pressed = True
                if event.key == pygame.K_d:
                    d_pressed = True
                if event.key == pygame.K_w:
                    w_pressed = True
                if event.key == pygame.K_s:
                    s_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    a_pressed = False
                if event.key == pygame.K_d:
                    d_pressed = False
                if event.key == pygame.K_w:
                    w_pressed = False
                if event.key == pygame.K_s:
                    s_pressed = False
            if event.type == pygame.MOUSEMOTION:
                x_mouse = event.pos[0]
                y_mouse = event.pos[1]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and x_mouse > x:
                camera.change_scale(True)
                speed = 15 / (2 - camera.scale)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and x_mouse > x:
                camera.change_scale(False)
                speed = 15 / (2 - camera.scale)
        if a_pressed:
            camera.dx += speed
        if d_pressed:
            camera.dx -= speed
        if w_pressed:
            camera.dy += speed
        if s_pressed:
            camera.dy -= speed

        if not paused:
            sprites_move(all_sprites, camera.dx, camera.dy, hor_borders, ver_borders)
            change_size_sprites(all_sprites, camera)

            move_projectiles(projectiles_group)
            money_kills, kills = enem_move(enemies_group, level_map, camera.scale, king)
            money_counter.count += money_kills
            all_money += money_kills
            all_kills += kills

            update_rect(sprites, screen)
            update_rect(enemies_group, screen)

            money_cats = cats_attack(cats_group, enemies_group, fps)
            money_counter.count += money_cats
            all_money += money_cats

            next_wave_btn.counter += 1 / fps
            spawner.check_to_spawn(new_wave=next_wave_btn.update())

            tray = check_cat_placed(sprites[0], choosen, x)
            if tray:
                spawn_cat(choosen, "tray", tray, tile_images, cat_images, projectiles_images, sprites[1], sprites[4],
                          all_sprites)
                for c in cards:
                    if c.name.text == choosen:
                        c.counter -= 1
                        if c.counter > 0:
                            break
                        else:
                            choosen = None
                            break
            check = check_cat_clicked(cats_group, x)
            if check is not None:
                if upgrade_menu_called is not None and upgrade_menu_called == check:
                    upgrade_menu_called = None
                    upgrade_menu = None
                else:
                    upgrade_menu_called = check
                    upgrade_menu = UpgradeMenu(10, 500 / 864 * full_h, upgrade_menu_called, cat_images)
            if upgrade_menu_called:
                upgrade_menu_updated = upgrade_menu.update(money_counter.count)
                if upgrade_menu_updated[0]:
                    if money_counter.count >= upgrade_menu_called.upgrade_cost:
                        money_counter.count -= upgrade_menu_called.upgrade_cost
                        upgrade_menu_called.upgrade()
                if upgrade_menu_updated[1]:
                    destroy_cat(upgrade_menu_called, sprites[1], sprites[4], tile_images, sprites[0], all_sprites)
                    upgrade_menu_called = None
                    upgrade_menu = None

            king.hp_bar.update(king.hp / king.max_hp)
            king.hp_bar.update_wave_text(spawner.wave)
            king.hp_bar.update_time_before_wave(round(spawner.time_before_wave))

            if king.hp == 0:
                running = False
                running_lose = True
        else:
            statistics = (all_kills, king.hp, all_money, spawner.wave)  # + level
            paused, back_to_menu, running = pause_menu.update()
            if back_to_menu:
                kill_all_sprites([*sprites, enemies_group, projectiles_group])
                return 2, statistics
            if not running:
                kill_all_sprites([*sprites, enemies_group, projectiles_group])
                return 0, statistics

        for i in sprites:
            i.draw(screen)
        enemies_group.draw(screen)
        projectiles_group.draw(screen)

        if upgrade_menu_called:
            if type(upgrade_menu_called).__name__ != "SunFlower":
                pygame.draw.circle(screen, "white", [upgrade_menu_called.rect[0] + upgrade_menu_called.rect[2] // 2,
                                                     upgrade_menu_called.rect[1] + upgrade_menu_called.rect[3] // 2],
                                   upgrade_menu_called.radius, 2)

        screen.blit(image1, rect1)
        screen.blit(image2, rect2)
        screen.blit(image3, rect3)
        screen.blit(image4, rect4)

        if not paused:
            chose, money = update_card(cards, screen, money=money_counter.count)
            money_counter.count = money
            if chose is not None:
                if chose == choosen:
                    choosen = None
                else:
                    choosen = chose

        money_counter.draw(screen)

        for card in cards:
            card.all_draw(screen)
        king.hp_bar.draw_health_bar()
        screen.blit(king.hp_bar.image, king.hp_bar.rect)
        screen.blit(king.hp_bar.text_hp_string_rendered, king.hp_bar.text_hp_rect)
        screen.blit(king.hp_bar.text_wave_string_rendered, king.hp_bar.text_wave_rect)
        screen.blit(king.hp_bar.text_time_before_wave_string_rendered, king.hp_bar.text_time_before_wave_rect)

        if upgrade_menu_called:
            upgrade_menu.draw(screen)

        ver_borders.draw(screen)
        hor_borders.draw(screen)
        next_wave_btn.draw(screen)

        if choosen and not paused:
            draw_neer_cursor(screen, cat_images[choosen])
        if paused:
            screen.blit(darken_surface, (0, 0))
            pause_menu.draw(screen)

        pygame.display.update()
        clock.tick(fps)

    while running_lose:
        statistics = (all_kills, king.hp, all_money, spawner.wave)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill_all_sprites([*sprites, enemies_group, projectiles_group])
                return 0, statistics
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    kill_all_sprites([*sprites, enemies_group, projectiles_group])
                    return 0, statistics
        screen.fill("gray")
        screen.blit(lose_image, lose_image.get_rect(center=screen.get_rect().center))
        pygame.display.update()
        clock.tick(fps)


def run_statistics(screen):
    info = pygame.display.Info()
    full_w = info.current_w
    full_h = info.current_h

    run_loading_screen = [True]
    scr_path = "\\".join(sys.argv[0].split("\\")[:-2])
    path = os.path.join(scr_path, "data", "other_images", "chipi_chipi_spritesheet.png")
    loading_screen_sprite = AnimatedSprite(load_image(path), 6, 6,
                                           full_w // 2, full_h // 2)
    t1 = Thread(target=loading_screen, args=(loading_screen_sprite, run_loading_screen, screen), daemon=True)
    t1.start()
    time.sleep(2)
    run_loading_screen[0] = False

    clock = pygame.time.Clock()
    fps = 60
    running = True
    stat_menu = StatisticsMenu(full_w, full_h)
    while running:
        screen.fill((40, 40, 40))
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                stat_menu.scroll(True)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                stat_menu.scroll(False)
        back_to_menu = stat_menu.update()
        if back_to_menu:
            return 2
        stat_menu.draw(screen)
        pygame.display.update()
        clock.tick(fps)


def main_menu(screen):
    info = pygame.display.Info()
    full_w = info.current_w
    full_h = info.current_h

    run_loading_screen = [True]
    scr_path = "\\".join(sys.argv[0].split("\\")[:-2])
    path = os.path.join(scr_path, "data", "other_images", "chipi_chipi_spritesheet.png")
    loading_screen_sprite = AnimatedSprite(load_image(path), 6, 6,
                                           full_w // 2, full_h // 2)
    t1 = Thread(target=loading_screen, args=(loading_screen_sprite, run_loading_screen, screen), daemon=True)
    t1.start()
    time.sleep(2)
    run_loading_screen[0] = False

    clock = pygame.time.Clock()
    fps = 60
    running = True
    menu = MainMenu(full_w // 2, full_h // 2)
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                return 0
        screen.fill((40, 40, 40))
        new_game_upd, ext_game_upd, stat_menu_upd, user = menu.update(event_list)
        if ext_game_upd:
            data = {"current_user": user}
            set_json(data, "current_user.json")
            return 0
        if new_game_upd:
            data = {"current_user": user}
            set_json(data, "current_user.json")
            return 1, user
        if stat_menu_upd:
            data = {"current_user": user}
            set_json(data, "current_user.json")
            return 3
        menu.draw(screen)

        pygame.display.update()
        clock.tick(fps)