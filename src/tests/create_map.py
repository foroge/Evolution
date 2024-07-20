import random
from stopit import threading_timeoutable

PATH_SYMB = "P"  # Символ пути внутри функций
ALT_PATH_SYMB = "-"  # Выходной символ пути
NONE_PATH_SYMB = "n"  # Символ запрета установки точки пути
GRASS_SYMB = "g"
KING_SYMB = "@"
SPAWN_SYMB = "#"
TRAY_SYMB = "T"
WATER_SYMB = "w"
TREE_SYMB = "t"
FENCE_SUMB = "F"
STONE_SYMB = "S"

RANDOM_GRASS_CHANCE = 0.05

level_map_to_return = None


def randomize_map_point(level_map, size, point1: tuple, point2: tuple, canstop=False):
    count = 0
    row = random.randint(max([point1[0], 0]), min([point2[0], size - 1]))
    col = random.randint(max([point1[1], 0]), min([point2[1], size - 1]))
    while level_map[row][col] != GRASS_SYMB:
        row = random.randint(max([point1[0], 0]), min([point2[0], size - 1]))
        col = random.randint(max([point1[1], 0]), min([point2[1], size - 1]))
        if canstop:
            count += 1
            if count > 25:
                return None
    return row, col


def create_path_corner(level_map, coords_start, coords_end):
    row, col = random.choice([(coords_start[0], coords_end[1]), (coords_end[0], coords_start[1])])
    if coords_start[0] != coords_end[0]:
        n = (coords_end[0] - coords_start[0]) // abs(coords_end[0] - coords_start[0])
        for i in range(coords_start[0], coords_end[0] + n, n):
            level_map[i][col] = PATH_SYMB
    if coords_start[1] != coords_end[1]:
        m = (coords_end[1] - coords_start[1]) // abs(coords_end[1] - coords_start[1])
        for i in range(coords_start[1] + m, coords_end[1] + m, m):
            level_map[row][i] = PATH_SYMB
    return level_map


def create_path(level_map, size, coords_king, coords_spawn):
    coords = coords_king
    end = False
    while not end:
        rad = 2.4
        rad_end = 3
        if abs(coords_spawn[0] - coords[0]) <= size // rad_end and abs(coords_spawn[1] - coords[1]) <= size // rad_end:
            point = coords_spawn
            end = True
        else:
            t = int(size // rad)
            for i in range(coords[0] - t, coords[0] + t):
                for j in range(coords[1] - 1, coords[1] + 1):
                    try:
                        if level_map[i][j] == GRASS_SYMB:
                            level_map[i][j] = NONE_PATH_SYMB
                    except IndexError:
                        ...
            for i in range(coords[0] - 1, coords[0] + 1):
                for j in range(coords[1] - t, coords[1] + t):
                    try:
                        if level_map[i][j] == GRASS_SYMB:
                            level_map[i][j] = NONE_PATH_SYMB
                    except IndexError:
                        ...
            point = randomize_map_point(level_map, size, (coords[0] - t, coords[1] - t),
                                        (coords[0] + t, coords[1] + t))
            for i in range(coords[0] - t, coords[0] + t):
                for j in range(coords[1] - 1, coords[1] + 1):
                    try:
                        if level_map[i][j] == NONE_PATH_SYMB:
                            level_map[i][j] = GRASS_SYMB
                    except IndexError:
                        ...
            for i in range(coords[0] - 1, coords[0] + 1):
                for j in range(coords[1] - t, coords[1] + t):
                    try:
                        if level_map[i][j] == NONE_PATH_SYMB:
                            level_map[i][j] = GRASS_SYMB
                    except IndexError:
                        ...
        level_map = create_path_corner(level_map, coords, point).copy()
        coords = point
    level_map[coords_king[0]][coords_king[1]] = KING_SYMB
    level_map[coords_spawn[0]][coords_spawn[1]] = SPAWN_SYMB
    return level_map


def create_empty_map(size):
    level_map = []
    for i in range(size):
        level_map.append([])
        for j in range(size):
            level_map[i].append(GRASS_SYMB)
    return level_map


def delete_useless_path_and_add_trays(level_map, coords_king, coords_spawn, add_tray=True):
    def check_neighbours(symb, r1, c1, direction1):
        if 0 <= r1 + direction1[0] < len(level_map) and 0 <= c1 + direction1[1] < len(level_map) and \
                level_map[r1 + direction1[0]][c1 + direction1[1]] == symb:
            direction1 = direction1
        elif 0 <= r1 - direction1[1] < len(level_map) and 0 <= c1 + direction1[0] < len(level_map) and \
                level_map[r1 - direction1[1]][c1 + direction1[0]] == symb:
            direction1 = -direction1[1], direction1[0]
        elif 0 <= r1 - direction1[0] < len(level_map) and 0 <= c1 - direction1[1] < len(level_map) and \
                level_map[r1 - direction1[0]][c1 - direction1[0]] == symb:
            direction1 = -direction1[0], -direction1[1]
        elif 0 <= r1 + direction1[1] < len(level_map) and 0 <= c1 - direction1[0] < len(level_map) and \
                level_map[r1 + direction1[1]][c1 - direction1[0]] == symb:
            direction1 = direction1[1], -direction1[0]
        else:
            direction1 = None
        return direction1

    def add_trays(r1, c1):
        for k in range(3):
            ret = randomize_map_point(level_map, len(level_map), (r1 - 2, c1 - 2), (r1 + 2, c1 + 2), True)
            if ret:
                level_map[ret[0]][ret[1]] = TRAY_SYMB if random.random() > 0.2 else WATER_SYMB
            else:
                break

    r, c = coords_spawn
    direction = None
    create_tray = 1
    while (r, c) != coords_king:
        if not direction:
            if 0 <= r - 1 < len(level_map) and 0 <= c < len(level_map) and level_map[r - 1][c] == PATH_SYMB:
                direction = -1, 0
            elif 0 <= r < len(level_map) and 0 <= c + 1 < len(level_map) and level_map[r][c + 1] == PATH_SYMB:
                direction = 0, 1
            elif 0 <= r + 1 < len(level_map) and 0 <= c < len(level_map) and level_map[r + 1][c] == PATH_SYMB:
                direction = 1, 0
            elif 0 <= r < len(level_map) and 0 <= c - 1 < len(level_map) and level_map[r][c - 1] == PATH_SYMB:
                direction = 0, -1
            r, c = r + direction[0], c + direction[1]
            level_map[r][c] = ALT_PATH_SYMB
        else:
            direct = check_neighbours(KING_SYMB, r, c, direction)
            if not direct:
                direct = check_neighbours(PATH_SYMB, r, c, direction)
            if not direct:
                direct = check_neighbours(ALT_PATH_SYMB, r, c, direction)
                if direct[0] == -direction[0] and direct[1] == -direction[1]:
                    direct = None
            if direct:
                direction = direct
                r, c = r + direction[0], c + direction[1]
                level_map[r][c] = ALT_PATH_SYMB
                if add_tray:
                    if create_tray % 2 == 0:
                        add_trays(r, c)
                    create_tray += 1
            else:
                level_map[r][c] = GRASS_SYMB
                r, c = r - direction[0], c - direction[1]

    for i in range(len(level_map)):
        for j in range(len(level_map[i])):
            if level_map[i][j] == PATH_SYMB:
                level_map[i][j] = GRASS_SYMB
    return level_map


def add_random_trays(level_map, size):
    for i in range(15):
        row, col = randomize_map_point(level_map, size, (0, 0), (size - 1, size - 1))
        level_map[row][col] = TRAY_SYMB if random.random() > 0.2 else WATER_SYMB
    return level_map


def randomize_grass(level_map, size):
    for i in range(size):
        for j in range(size):
            if level_map[i][j] == GRASS_SYMB:
                if random.random() <= RANDOM_GRASS_CHANCE:
                    level_map[i][j] = TREE_SYMB
                if random.random() <= RANDOM_GRASS_CHANCE:
                    level_map[i][j] = FENCE_SUMB
                if random.random() <= RANDOM_GRASS_CHANCE:
                    level_map[i][j] = STONE_SYMB
    return level_map


def add_stone_border(level_map, size):
    stone_border = [STONE_SYMB for _ in range(size + 2)]
    level_map.insert(0, stone_border)
    for i in range(1, size + 1):
        level_map[i].insert(0, STONE_SYMB)
        level_map[i].append(STONE_SYMB)
    level_map.append(stone_border)
    return level_map


@threading_timeoutable()
def create_map(size):
    global level_map_to_return

    size = size - 2
    level_map = create_empty_map(size).copy()
    half_y = random.choice([-1, 1])
    half_x = random.choice([-1, 1])
    row_king = size // 2 - random.randint(size // 4, size // 2 - 1) * half_y
    col_king = size // 2 - random.randint(size // 4, size // 2 - 1) * half_x
    level_map[row_king][col_king] = KING_SYMB
    row_spawn = size // 2 - random.randint(size // 4, size // 2 - 1) * [0, -1, 1][half_y:][0]
    col_spawn = size // 2 - random.randint(size // 4, size // 2 - 1) * [0, -1, 1][half_x:][0]
    level_map[row_spawn][col_spawn] = SPAWN_SYMB

    bad = True
    while bad:
        try:
            level_map = create_path(level_map, size, (row_king, col_king), (row_spawn, col_spawn)).copy()
            while sum(list(map(lambda x: x.count(PATH_SYMB), level_map))) > 100:
                level_map = create_empty_map(size).copy()
                level_map[row_king][col_king] = KING_SYMB
                level_map[row_spawn][col_spawn] = SPAWN_SYMB
                level_map = create_path(level_map, size, (row_king, col_king), (row_spawn, col_spawn)).copy()
            level_map = delete_useless_path_and_add_trays(level_map, (row_king, col_king),
                                                          (row_spawn, col_spawn)).copy()
            level_map[row_king][col_king] = KING_SYMB

            for k in range(2):
                for i in range(len(level_map)):
                    for j in range(len(level_map[i])):
                        if level_map[i][j] == ALT_PATH_SYMB:
                            level_map[i][j] = PATH_SYMB

                level_map = delete_useless_path_and_add_trays(level_map, (row_king, col_king), (row_spawn, col_spawn),
                                                              add_tray=False).copy()
                level_map[row_king][col_king] = KING_SYMB

            level_map = add_random_trays(level_map, size).copy()
            level_map = randomize_grass(level_map, size).copy()

            bad = False
        except BaseException:
            level_map = create_empty_map(size).copy()
            level_map[row_king][col_king] = KING_SYMB
            level_map[row_spawn][col_spawn] = SPAWN_SYMB
            bad = True

    level_map = add_stone_border(level_map, size)
    level_map_to_return = level_map.copy()

    return True


def start_creating(size):
    if create_map(size, timeout=2):
        return level_map_to_return
    return start_creating(size)
