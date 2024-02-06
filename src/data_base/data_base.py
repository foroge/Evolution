import sqlite3 as db
import os
import sys
import datetime as dt
import pygame

STAT_DDl = """
    CREATE TABLE statistics (
        id INTEGER,
        kills INTEGER,
        difficulty INTEGER,
        money INTEGER,
        wave INTEGER,
        level INTEGER
    );
"""


TIME_DDL = """
    CREATE TABLE time (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        date TEXT,
        user TEXT
    );
"""


class DataBase:
    def __init__(self):
        scr_path = "\\".join(sys.argv[0].split("\\")[:-2])
        path = os.path.join(scr_path, "data", "data_base", "statistics.db")
        self.base = db.connect(path)
        self.add_table()

    def add_table(self):
        len_stat = self.base.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='statistics'")
        len_time = self.base.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='time'")
        self.create_table(len_time, STAT_DDl)
        self.create_table(len_stat, TIME_DDL)

    def create_table(self, len_table, ddl):
        for length in len_table:
            with self.base:
                cur = self.base.cursor()
                if length[0] == 0:
                    cur.execute(ddl)
                cur.close()

    def save_to_db(self, parameters, user):
        sql_to_stat = "INSERT INTO statistics (id, kills, difficulty, money, wave, level) VALUES (?, ?, ?, ?, ?, ?)"
        date, time = str(dt.date.today()), str(dt.datetime.now().time().strftime("%H:%M"))
        with self.base:
            cur = self.base.cursor()
            sql = cur.execute(f"SELECT * FROM time WHERE date = '{date}' AND time = '{time}' AND user = '{user}'")
            if len([*sql]) > 0:
                self.change_stat(parameters, date, time, user)
            else:
                sql_to_time = f"INSERT INTO time (time, date, user) VALUES ('{time}', '{date}', '{user}')"
                cur.execute(sql_to_time)
                id_element = self.get_id_db(date, time, user)
                print(parameters)
                cur.execute(sql_to_stat, (id_element, *parameters))
            cur.close()

    def get_id_db(self, date, time, user):
        sql = f"SELECT id FROM time WHERE date = '{date}' AND time = '{time}' AND user = '{user}'"
        with self.base:
            cur = self.base.cursor()
            text_id = cur.execute(sql)
            id_rec = text_id.fetchone()
            cur.close()
            return int(id_rec[0])

    def get_record_db(self, date, time, user):
        id_element = self.get_id_db(date, time, user)
        sql_stat = f"SELECT * FROM statistics WHERE id = '{id_element}'"
        with self.base:
            cur = self.base.cursor()
            stats = [i[0] for i in cur.execute(sql_stat)]
            cur.close()
            return [user, date, time, *stats]

    def get_all_id_db(self, user=None, old_date=None, cur_date=None):
        if not old_date:
            old_date = "0000-00-00"
        if not cur_date:
            cur_date = "9999-99-99"
        user_sql = f"user = '{user}' AND " if user else " "
        date_sql = f"(date >= '{old_date}') AND (date <= '{cur_date}')"
        sql = f"SELECT id FROM time WHERE {user_sql}{date_sql}"
        with self.base:
            cur = self.base.cursor()
            all_id = sorted([str(i[0]) for i in cur.execute(sql)])
            cur.close()
            return all_id

    def get_all_stat_db(self):
        all_stat_sql = (f"SELECT time.user, time.date, time.time, statistics.difficulty, statistics.level, "
                        f"statistics.wave, statistics.kills, statistics.money FROM statistics, "
                        f"time WHERE time.id == statistics.id ORDER BY time.id DESC")
        with self.base:
            cur = self.base.cursor()
            all_stat = sorted(list(cur.execute(all_stat_sql)), reverse=True)
            cur.close()
            return all_stat

    def change_stat(self, parameters, date, time, user):
        id_element = self.get_id_db(date, time, user)
        with self.base:
            cur = self.base.cursor()
            self.del_from_db(date, time, user)
            sql_to_stat = "INSERT INTO statistics (id, kills, difficulty, money, wave, level) VALUES (?, ?, ?, ?, ?, ?)"
            cur.execute(sql_to_stat, (id_element, *parameters))
            cur.close()

    def del_from_db(self, date, time, user):
        id_element = self.get_id_db(date, time, user)
        with self.base:
            cur = self.base.cursor()
            sql_stat = f"DELETE FROM statistics WHERE id = '{id_element}'"
            sql_time = f"DELETE FROM time WHERE id = '{id_element}'"
            cur.execute(sql_stat)
            cur.execute(sql_time)
            cur.close()

    def del_all(self):
        sql_del_id = "SELECT id FROM time"
        sql_stat = f"DELETE FROM statistics WHERE id IN ({sql_del_id})"
        sql_time = f"DELETE FROM time WHERE id IN ({sql_del_id})"
        with self.base:
            cur = self.base.cursor()
            cur.execute(sql_stat)
            cur.execute(sql_time)
            cur.close()


class DBViewer:
    def __init__(self, x, y, full_w, full_h, stat=tuple()):
        self.db = DataBase()
        self.font_height = full_h // 40
        self.font = pygame.font.SysFont("Monospace", self.font_height)
        self.stat = stat
        self.x = x
        self.y = y
        self.full_width = full_w
        self.full_height = full_h
        self.size = self.y + 35 + len(self.db.get_all_stat_db()) * self.font_height + 6

    def draw(self, screen, y=0):
        heads = {"User": 20, "Date": 8, "Time": 5, "difficulty": 10, "Level": 6, "Wave": 6, "Kills": 6, "Money": 8}
        heads_list = list(heads.keys())
        divider_w = sum(heads.values())
        size_w = self.full_width * 0.75 / divider_w
        rows = self.db.get_all_stat_db()
        if self.stat:
            heads_list = heads_list[3:]
            rows = [self.stat]
        for i, row in enumerate(rows):
            size_row = 0
            for j, col in enumerate(row):
                size_text = size_w * heads[heads_list[j]]
                cell = self.font.render(str(col), True, "yellow")
                screen.blit(cell, [self.x + size_row, self.y + y + 35 + i * self.font_height + 6])
                size_row += size_text
        pygame.draw.rect(screen, (40, 40, 40), [(0, 0), (self.full_width, 80)])
        size_row = 0
        for i, head in enumerate(heads.keys() if not self.stat else list(heads.keys())[3:]):
            size_text = size_w * heads[head]
            head = self.font.render(head, True, "yellow")
            screen.blit(head, [self.x + size_row, self.y])
            size_row += size_text

    def get_y_size(self):
        return self.size
