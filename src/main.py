import pygame
import sys
import os

from run_game.run_function import main_menu, game, run_statistics
from data_base.data_base import DataBase
from extra_utils import get_json

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
    src_path = "\\".join(sys.argv[0].split("\\")[:-2])
    json = get_json(os.path.join(src_path, "data", "current_user.json"))
    user = json["current_user"]
    statistics = []
    if ret_code != 0:
        while all_running:
            if type(eval(str(ret_code))) != int:
                if type(eval(str(ret_code))[1]) == str:
                    user = ret_code[1]
                else:
                    statistics = ret_code[1]
                    data_base.save_to_db(statistics, user)
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
