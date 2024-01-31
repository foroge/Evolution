import pygame

from run_game.run_function import main_menu, game, run_statistics
from data_base.data_base import DataBase

pygame.init()
pygame.font.init()

info = pygame.display.Info()
full_w = info.current_w
full_h = info.current_h
screen = pygame.display.set_mode((full_w, full_h))
data_base = DataBase()

if __name__ == "__main__":
    all_running = True
    ret_code = main_menu(screen)
    user = ""
    statistics = []
    if ret_code != 0:
        while all_running:
            if len(eval(str(ret_code))) > 1:
                if type(eval(str(ret_code))[1]) == str:
                    user = ret_code[1]
                else:
                    statistics = ret_code[1]
                    print("ok1")
                    data_base.save_to_db(statistics, user)
                    print("ok2")
                    print(data_base.get_all_stat_db())

                ret_code = ret_code[0]
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
