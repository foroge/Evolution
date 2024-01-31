import sqlite3
import os
import datetime as dt

STAT_DDl = """
    CREATE TABLE statistics (
        id INTEGER,
        kills INTEGER,
        health INTEGER,
        money INTEGER,
        wave INTEGER,
        level INTEGER,
)"""


TIME_DDL = """
    CREATE TABLE time (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        date TEXT,
        user TEXT
    );"""


class DataBase:
    def __init__(self):
        scr_path = "\\".join(sys.argv[0].split("\\")[:-2])
        path = os.path.join(scr_path, "data_base", "statistics.db")
        self.base = bd.connect(path)
        self.add_table()

    def add_table(self):
        with self.base:
            len_stat = self.base.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='statistics'")
            len_time = self.base.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='time'")
            self.create_table(len_stat, STAT_DDl)
            self.create_table(len_time, TIME_DDL)

    def create_table(self, len_table, ddl):
        for length in len_table:
            with self.base:
                if length[0] == 0:
                    self.base.execute(ddl)

    def save_to_db(self, parameters, user):
        sql_to_time = f"INSERT INTO time (time, date, user) VALUES (?, ?, ?)"
        sql_to_stat = f"INSERT INTO statistics (id, kills, health, money, wave, level) VALUES (?, ?, ?, ?, ?, ?)"
        with self.base:
            date, time = str(dt.date.today()), str(dt.datetime.now().time().strftime("%H:%M"))
            sql = self.base.execute(f"SELECT * FROM time WHERE date = '{date}' AND time = '{time}' AND user = '{user}'")
            if len([*sql]) > 0:
                self.change_stat(parameters, date, time, user)
            else:
                self.base.execute(sql_to_time, (date, time, user))
                id_element = self.get_id_db(date, time, user)
                self.base.execute(sql_to_stat, (id_element, *parameters))

    def get_id_db(self, date, time, user):
        sql = f"SELECT id FROM time WHERE date = '{date}' AND time = '{time}' AND user = '{user}'"
        with self.base:
            text_id = self.base.execute(sql)
            id_rec = [*text_id]
            return int(id_rec[0])

    def get_record_db(self, date, time, user):
        id_element = self.get_id_db(date, time, user)
        sql_stat = f"SELECT * FROM statistics WHERE id = '{id_element}'"
        with self.base:
            stats = [i[0] for i in self.base.execute(sql_stat)]
        return [user, date, time, *stats]

    def get_all_id_db(self, user=None, old_date=None, cur_date=None):
        if not old_date:
            old_date = "0000-00-00"
        if not cur_date:
            cur_date = "9999-99-99"
        user_sql = f"user = '{user}' " if user else ""
        date_sql = f"(date >= '{old_date}') AND (date <= '{cur_date}')"
        sql = f"SELECT id FROM time WHERE {user_sql}AND {date_sql}"
        with self.base:
            all_id = sorted(list(self.base.execute(sql)))
            return all_id

    def get_all_stat_db(self, user=None, old_date=None, cur_date=None):
        all_id = get_all_id_db(user, old_date, cur_date)
        all_id = ', '.join(all_id)
        all_stat_sql = f"SELECT * FROM statistics WHERE id IN ({all_id})"
        with self.base:
            all_stat = sorted(list(self.base.execute(all_stat_sql)), reverse=True)
        return all_stat

    def change_stat(self, parameters, date, time, user):
        id_element = self.get_id_db(date, time, user)
        with self.base:
            sql = f"INSERT INTO statistics ({id_element}, {', '.join(parameters)})"
            self.base.execute(sql)

    def del_from_db(self, date, time, user):
        id_element = self.get_id_db(date, time, user)
        with self.base:
            sql_stat = f"DELETE FROM statistics WHERE id = '{id_element}'"
            sql_time = f"DELETE FROM time WHERE id = '{id_element}'"
            self.base.execute(sql_stat)
            self.base.execute(sql_time)

    def del_all(self, user):
        with self.base:
            sql_del_id = f"SELECT id FROM time"
            sql_stat = f"DELETE FROM statistics WHERE id IN ({sql_del_id})"
            sql_time = f"DELETE FROM time WHERE id IN ({sql_del_id})"
            self.base.execute(sql_stat)
            self.base.execute(sql_time)