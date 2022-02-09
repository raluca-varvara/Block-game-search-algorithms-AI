def blockGoalPosition(block, no_puzzle):
    position = (0, 0)
    if no_puzzle == 1:
        if block == 0:
            position = (0, 1)
        if block == 1:
            position = (0, 0)
        if block == 2:
            position = (1, 0)

    if no_puzzle == 2:
        if block == 0:
            position = (0, 1)
        if block == 1:
            position = (1, 1)
        if block == 2:
            position = (0, 0)
        if block == 3:
            position = (1, 0)
        if block == 4:
            position = (2, 0)

    if no_puzzle == 3:
        if block == 0:
            position = (0, 1)
        if block == 1:
            position = (2, 1)
        if block == 2:
            position = (0, 0)
        if block == 3:
            position = (1, 0)
        if block == 4:
            position = (1, 1)
        if block == 5:
            position = (2, 0)

    return position


def manhattanHeuristic(position, block, no_puzzle):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = blockGoalPosition(block, no_puzzle)
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclideanHeuristic(position, block, no_puzzle):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = blockGoalPosition(block, no_puzzle)
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


def chebisevDistance(position, block, no_puzzle):
    xy1 = position
    xy2 = blockGoalPosition(block, no_puzzle)
    d = max((xy1[0] - xy2[0]), (xy1[1] - xy2[1]))
    return d


def chiSquaredDistance(position, block, no_puzzle):
    xy1 = position
    xy2 = blockGoalPosition(block, no_puzzle)
    s0 = xy1[0] + xy2[0]
    s1 = xy1[1] + xy2[1]
    if s0 == 0:
        s0 = 1
    if s1 == 0:
        s1 = 1
    d = 0.5 * (((xy1[0] - xy2[0]) ** 2) / (s0)
               + ((xy1[1] - xy2[1]) ** 2) / (s1))
    return d