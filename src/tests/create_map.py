import random

PATH_SYMB = "P"  # Символ пути внутри функций
ALT_PATH_SYMB = "-"  # Выходной символ пути
GRASS_SYMB = "g"
KING_SYMB = "@"
SPAWN_SYMB = "#"
TRAY_SYMB = "T"
WATER_SYMB = "w"
TREE_SYMB = "t"
FENCE_SUMB = "F"
STONE_SYMB = "S"


def randomize_map_point(levelMap, size, point1: tuple, point2: tuple, canstop=False):
    count = 0
    row = random.randint(max([point1[0], 0]), min([point2[0], size - 1]))
    col = random.randint(max([point1[1], 0]), min([point2[1], size - 1]))
    while levelMap[row][col] != GRASS_SYMB:
        row = random.randint(max([point1[0], 0]), min([point2[0], size - 1]))
        col = random.randint(max([point1[1], 0]), min([point2[1], size - 1]))
        if canstop:
            count += 1
            if count > 25:
                return None
    return row, col


def create_path_corner(levelMap, coordsStart, coordsEnd):
    row, col = random.choice([(coordsStart[0], coordsEnd[1]), (coordsEnd[0], coordsStart[1])])
    if coordsStart[0] != coordsEnd[0]:
        n = (coordsEnd[0] - coordsStart[0]) // abs(coordsEnd[0] - coordsStart[0])
        for i in range(coordsStart[0], coordsEnd[0] + n, n):
            levelMap[i][col] = PATH_SYMB
    if coordsStart[1] != coordsEnd[1]:
        m = (coordsEnd[1] - coordsStart[1]) // abs(coordsEnd[1] - coordsStart[1])
        for i in range(coordsStart[1] + m, coordsEnd[1] + m, m):
            levelMap[row][i] = PATH_SYMB
    return levelMap


def create_path(levelMap, size, coordsKing, coordsSpawn):
    coords = coordsKing
    end = False
    while not end:
        rad = 2
        if abs(coordsSpawn[0] - coords[0]) <= size // rad and abs(coordsSpawn[1] - coords[1]) <= size // rad:
            point = coordsSpawn
            end = True
        else:
            point = randomize_map_point(levelMap, size, (coords[0] - size // rad, coords[1] - size // rad),
                                      (coords[0] + size // rad, coords[1] + size // rad))
        levelMap = create_path_corner(levelMap, coords, point).copy()
        coords = point
    levelMap[coordsKing[0]][coordsKing[1]] = KING_SYMB
    levelMap[coordsSpawn[0]][coordsSpawn[1]] = SPAWN_SYMB
    return levelMap


def create_empty_map(size):
    levelMap = []
    for i in range(size):
        levelMap.append([])
        for j in range(size):
            levelMap[i].append(GRASS_SYMB)
    return levelMap


def delete_useless_path_and_add_trays(levelMap, coordsKing, coordsSpawn):
    def check_neighbours(symb, r, c, direction):
        if 0 <= r + direction[0] < len(levelMap) and 0 <= c + direction[1] < len(levelMap) and \
                levelMap[r + direction[0]][c + direction[1]] == symb:
            direction = direction
        elif 0 <= r - direction[1] < len(levelMap) and 0 <= c + direction[0] < len(levelMap) and \
                levelMap[r - direction[1]][c + direction[0]] == symb:
            direction = -direction[1], direction[0]
        elif 0 <= r - direction[0] < len(levelMap) and 0 <= c - direction[1] < len(levelMap) and \
                levelMap[r - direction[0]][c - direction[0]] == symb:
            direction = -direction[0], -direction[1]
        elif 0 <= r + direction[1] < len(levelMap) and 0 <= c - direction[0] < len(levelMap) and \
                levelMap[r + direction[1]][c - direction[0]] == symb:
            direction = direction[1], -direction[0]
        else:
            direction = None
        return direction

    def add_trays(r, c):
        for k in range(3):
            ret = randomize_map_point(levelMap, len(levelMap), (r - 2, c - 2), (r + 2, c + 2), True)
            if ret:
                levelMap[ret[0]][ret[1]] = TRAY_SYMB if random.random() > 0.2 else WATER_SYMB
            else:
                break

    r, c = coordsSpawn
    direction = None
    create_tray = 1
    while (r, c) != coordsKing:
        if not direction:
            if 0 <= r - 1 < len(levelMap) and 0 <= c < len(levelMap) and levelMap[r - 1][c] == PATH_SYMB:
                direction = -1, 0
            elif 0 <= r < len(levelMap) and 0 <= c + 1 < len(levelMap) and levelMap[r][c + 1] == PATH_SYMB:
                direction = 0, 1
            elif 0 <= r + 1 < len(levelMap) and 0 <= c < len(levelMap) and levelMap[r + 1][c] == PATH_SYMB:
                direction = 1, 0
            elif 0 <= r < len(levelMap) and 0 <= c - 1 < len(levelMap) and levelMap[r][c - 1] == PATH_SYMB:
                direction = 0, -1
            r, c = r + direction[0], c + direction[1]
            levelMap[r][c] = ALT_PATH_SYMB
        else:
            dir = check_neighbours(KING_SYMB, r, c, direction)
            if not dir:
                dir = check_neighbours(PATH_SYMB, r, c, direction)
            if not dir:
                dir = check_neighbours(ALT_PATH_SYMB, r, c, direction)
                if dir[0] == -direction[0] and dir[1] == -direction[1]:
                    dir = None
            if dir:
                direction = dir
                r, c = r + direction[0], c + direction[1]
                levelMap[r][c] = ALT_PATH_SYMB
                if create_tray % 2 == 0:
                    add_trays(r, c)
                create_tray += 1
            else:
                levelMap[r][c] = GRASS_SYMB
                r, c = r - direction[0], c - direction[1]

    for i in range(len(levelMap)):
        for j in range(len(levelMap[i])):
            if levelMap[i][j] == PATH_SYMB:
                levelMap[i][j] = GRASS_SYMB
    return levelMap


def add_random_trays(levelMap, size):
    for i in range(15):
        row, col = randomize_map_point(levelMap, size, (0, 0), (size - 1, size - 1))
        levelMap[row][col] = TRAY_SYMB if random.random() > 0.2 else WATER_SYMB
    return levelMap


def randomize_grass(levelMap, size):
    for i in range(size):
        for j in range(size):
            if levelMap[i][j] == GRASS_SYMB:
                if random.random() <= 0.05:
                    levelMap[i][j] = TREE_SYMB
                if random.random() <= 0.05:
                    levelMap[i][j] = FENCE_SUMB
                if random.random() <= 0.05:
                    levelMap[i][j] = STONE_SYMB
    return levelMap


def create_map(size):
    levelMap = create_empty_map(size).copy()
    halfY = random.choice([-1, 1])
    halfX = random.choice([-1, 1])
    rowKing = size // 2 - random.randint(size // 4, size // 2 - 1) * halfY
    colKing = size // 2 - random.randint(size // 4, size // 2 - 1) * halfX
    levelMap[rowKing][colKing] = KING_SYMB
    rowSpawn = size // 2 - random.randint(size // 4, size // 2 - 1) * [0, -1, 1][halfY:][0]
    colSpawn = size // 2 - random.randint(size // 4, size // 2 - 1) * [0, -1, 1][halfX:][0]
    levelMap[rowSpawn][colSpawn] = SPAWN_SYMB

    bad = True
    while bad:
        try:
            levelMap = create_path(levelMap, size, (rowKing, colKing), (rowSpawn, colSpawn)).copy()
            while sum(list(map(lambda x: x.count(PATH_SYMB), levelMap))) > 100:
                levelMap = create_empty_map(size).copy()
                levelMap[rowKing][colKing] = KING_SYMB
                levelMap[rowSpawn][colSpawn] = SPAWN_SYMB
                levelMap = create_path(levelMap, size, (rowKing, colKing), (rowSpawn, colSpawn)).copy()
            levelMap = delete_useless_path_and_add_trays(levelMap, (rowKing, colKing), (rowSpawn, colSpawn)).copy()
            levelMap[rowKing][colKing] = KING_SYMB

            levelMap = add_random_trays(levelMap, size).copy()
            levelMap = randomize_grass(levelMap, size).copy()

            bad = False
        except Exception:
            levelMap = create_empty_map(size).copy()
            levelMap[rowKing][colKing] = KING_SYMB
            levelMap[rowSpawn][colSpawn] = SPAWN_SYMB
            bad = True
    return levelMap


if __name__ == "__main__":
    print(*create_map(32), sep="\n")
