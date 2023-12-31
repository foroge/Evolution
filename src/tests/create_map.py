import random

PATH_SYMB = "-"
ALT_PATH_SYMB = "P"
GRASS_SYMB = " "


def randomize_map_point(levelMap, size, point1: tuple, point2: tuple):
    row = random.randint(max([point1[0], 0]), min([point2[0], size - 1]))
    col = random.randint(max([point1[1], 0]), min([point2[1], size - 1]))
    while levelMap[row][col] != GRASS_SYMB:
        row = random.randint(max([point1[0], 0]), min([point2[0], size - 1]))
        col = random.randint(max([point1[1], 0]), min([point2[1], size - 1]))
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
    levelMap[coordsKing[0]][coordsKing[1]] = "@"
    levelMap[coordsSpawn[0]][coordsSpawn[1]] = "#"
    return levelMap


def create_empty_map(size):
    levelMap = []
    for i in range(size):
        levelMap.append([])
        for j in range(size):
            levelMap[i].append(GRASS_SYMB)
    return levelMap


def delete_useless_path(levelMap, coordsKing, coordsSpawn):
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

    r, c = coordsSpawn
    direction = None
    while (r, c) != coordsKing:
        if not direction:
            if 0 <= r - 1 < len(levelMap) and 0 <= c < len(levelMap) and levelMap[r - 1][c] == "-":
                direction = -1, 0
            elif 0 <= r < len(levelMap) and 0 <= c + 1 < len(levelMap) and levelMap[r][c + 1] == "-":
                direction = 0, 1
            elif 0 <= r + 1 < len(levelMap) and 0 <= c < len(levelMap) and levelMap[r + 1][c] == "-":
                direction = 1, 0
            elif 0 <= r < len(levelMap) and 0 <= c - 1 < len(levelMap) and levelMap[r][c - 1] == "-":
                direction = 0, -1
            r, c = r + direction[0], c + direction[1]
            levelMap[r][c] = ALT_PATH_SYMB
        else:
            # if 0 <= r + direction[0] < len(levelMap) and 0 <= c + direction[1] < len(levelMap) and \
            #         levelMap[r + direction[0]][c + direction[1]] == PATH_SYMB:
            #     direction = direction
            # elif 0 <= r - direction[1] < len(levelMap) and 0 <= c + direction[0] < len(levelMap) and \
            #         levelMap[r - direction[1]][c + direction[0]] == PATH_SYMB:
            #     direction = -direction[1], direction[0]
            # elif 0 <= r - direction[0] < len(levelMap) and 0 <= c - direction[1] < len(levelMap) and \
            #         levelMap[r - direction[0]][c - direction[0]] == PATH_SYMB:
            #     direction = -direction[0], -direction[1]
            # elif 0 <= r + direction[1] < len(levelMap) and 0 <= c - direction[0] < len(levelMap) and \
            #         levelMap[r + direction[1]][c - direction[0]] == PATH_SYMB:
            #     direction = direction[1], -direction[0]
            dir = check_neighbours("@", r, c, direction)
            if not dir:
                dir = check_neighbours(PATH_SYMB, r, c, direction)
            if dir:
                direction = dir
                r, c = r + direction[0], c + direction[1]
                levelMap[r][c] = ALT_PATH_SYMB
            else:
                levelMap[r + direction[0]][c + direction[1]] = GRASS_SYMB
                r, c = r - direction[0], c - direction[1]

    for i in range(len(levelMap)):
        for j in range(len(levelMap[i])):
            if levelMap[i][j] == PATH_SYMB:
                levelMap[i][j] = GRASS_SYMB
    return levelMap


def create_map(size):
    levelMap = create_empty_map(size).copy()
    halfY = random.choice([-1, 1])
    halfX = random.choice([-1, 1])
    rowKing = size // 2 - random.randint(size // 4, size // 2 - 1) * halfY
    colKing = size // 2 - random.randint(size // 4, size // 2 - 1) * halfX
    levelMap[rowKing][colKing] = "@"
    rowSpawn = size // 2 - random.randint(size // 4, size // 2 - 1) * [0, -1, 1][halfY:][0]
    colSpawn = size // 2 - random.randint(size // 4, size // 2 - 1) * [0, -1, 1][halfX:][0]
    levelMap[rowSpawn][colSpawn] = "#"
    levelMap = create_path(levelMap, size, (rowKing, colKing), (rowSpawn, colSpawn)).copy()
    while sum(list(map(lambda x: x.count(PATH_SYMB), levelMap))) > 100:
        levelMap = create_empty_map(size).copy()
        levelMap[rowKing][colKing] = "@"
        levelMap[rowSpawn][colSpawn] = "#"
        levelMap = create_path(levelMap, size, (rowKing, colKing), (rowSpawn, colSpawn)).copy()
    levelMap = delete_useless_path(levelMap, (rowKing, colKing), (rowSpawn, colSpawn)).copy()
    levelMap[rowKing][colKing] = "@"
    return levelMap


if __name__ == "__main__":
    print(*create_map(32), sep="\n")
