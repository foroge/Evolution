import pygame

from run_game.run_function import main_menu, game, run_statistics

pygame.init()
pygame.font.init()

info = pygame.display.Info()
full_w = info.current_w
full_h = info.current_h
screen = pygame.display.set_mode((full_w, full_h))

if __name__ == "__main__":
    all_running = True
    ret_code = main_menu(screen)
    if ret_code != 0:
        while all_running:
            if ret_code == 0:
                all_running = False
            if ret_code == 1:
                ret_code = game(screen)
            if ret_code == 2:
                ret_code = main_menu(screen)
            if ret_code == 3:
                ret_code = run_statistics(screen)
    pygame.quit()
    quit()
