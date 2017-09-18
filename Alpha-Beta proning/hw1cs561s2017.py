import sys
import copy

inputfile = sys.argv[1]

player = ""   # First player to move
opponent = ""  # The other player
cutOffDepth = 0

p_inf = float("inf")
n_inf = -float("inf")

log = list()  # output log
init_state = []

# Initial weights in the grid
weights = [[99, -8, 8, 6, 6, 8, -8, 99],
     [-8, -24, -4, -3, -3, -4, -24, -8],
     [8, -4, 7, 4, 4, 7, -4, 8],
     [6, -3, 4, 0, 0, 4, -3, 6],
     [6, -3, 4, 0, 0, 4, -3, 6],
     [8, -4, 7, 4, 4, 7, -4, 8],
     [-8, -24, -4, -3, -3, -4, -24, -8],
     [99, -8, 8, 6, 6, 8, -8, 99]]

with open(inputfile, "r")as infile:
    data = infile.read()

line = data.splitlines()

# Initial the first player to move and cut_off depth
player = line[0]
if player == 'X':
    opponent = 'O'
else:
    opponent = 'X'

cutOffDepth = int(line[1])


# Initial state
for i in range(2, len(line)):
    state = []
    for s in line[i].rstrip():
        state.append(s)
    init_state.append(state)


# Check if game ends
def check_end(states):
    playerNum = 0
    opponentNum = 0

    for i in range(0, 8):
        for j in range(0, 8):
            if states[i][j] == player:
                playerNum += 1
            if states[i][j] == opponent:
                opponentNum += 1
    if playerNum * opponentNum == 0 or playerNum + opponentNum == 64:
        return True

    return False


# get the value of current state
def evaluation(states):
    value = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if states[i][j] == player:
                value += weights[i][j]
            if states[i][j] == opponent:
                value -= weights[i][j]
    return value


# Check if the nmove is on board
def on_board(x, y):
    return x in range(0, 8) and y in range(0, 8)


# Transform node in the format we wanna print
def get_node(node):
    print_coord = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return print_coord[node[1]]+str(node[0]+1)


# check if this move is valid for current player
def check_valid(state, x, y, ply):
    if ply == "X":
        oppo = "O"
    else:
        oppo = "X"
    if state[x][y] != "*":
        return False
    # There are eight potential direction that may have opponent's pieces
    for direct_x, direct_y in [1, -1], [1, 0], [1, 1], [0, -1], [0, 1], [-1, -1], [-1, 0], [-1, 1]:
        temp_x, temp_y = x+direct_x, y+direct_y
        if on_board(temp_x, temp_y) and state[temp_x][temp_y] == oppo:
            while on_board(temp_x, temp_y):
                if state[temp_x][temp_y] != oppo:
                    break
                temp_x += direct_x
                temp_y += direct_y

            if on_board(temp_x, temp_y) and state[temp_x][temp_y] == ply:
                return True
    return False


# get all valid moves
def get_valid_moves(state, ply):
    child = []
    for i in range(0, 8):
        for j in range(0, 8):
            if check_valid(state, i, j, ply):
              child.append((i, j))
    return child


# generate next state from the coordinates and current player
def get_next_state(state, coord, ply):
    next_state = state
    x = coord[0]
    y = coord[1]
    if ply == player:
        oppo = opponent
    else:
        oppo = player
    next_state[x][y] = ply
    for direct_x, direct_y in [1, -1], [1, 0], [1, 1], [0, -1], [0, 1], [-1, -1], [-1, 0], [-1, 1]:
        temp_x, temp_y = copy.deepcopy(x+direct_x), copy.deepcopy(y+direct_y)
        if on_board(temp_x, temp_y) and next_state[temp_x][temp_y] == oppo:
            while on_board(temp_x, temp_y):
                if next_state[temp_x][temp_y] != oppo:
                    break
                temp_x += direct_x
                temp_y += direct_y
            if on_board(temp_x, temp_y) and next_state[temp_x][temp_y] == ply:
                m = copy.deepcopy(x+direct_x)
                n = copy.deepcopy(y+direct_y)
                while next_state[m][n] != ply:
                    next_state[m][n] = ply
                    m += direct_x
                    n += direct_y



    return next_state


# process alpha beta when they are infinity
def process(value):
    if value == p_inf:
        return "Infinity"
    elif value == n_inf:
        return "-Infinity"
    else:
        return value


# max value
def max_value(state, node, depth, alpha, beta):
    if node == "root":
        print_node = "root"
    elif node == "pass" or node == "end":
        print_node = "pass"
    else:
        print_node = get_node(node)
    if depth >= cutOffDepth or node == "end":
        log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, evaluation(state), process(alpha), process(beta)))
        return evaluation(state), "end"
 #   if check_end(state):
 #       log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, evaluation(state), process(alpha), process(beta)))
  #      return evaluation(state), "end"
    value = n_inf
    child = get_valid_moves(state, player)
    if not child:
        log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
        # if both sides pass their move, the game is end
        if print_node == "pass":
            next_node = "end"
        else:
            next_node = "pass"
        value = max(value, min_value(copy.deepcopy(state), next_node, depth+1, alpha, beta)[0])
        if value >= beta:
            log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
            return value, "pass"
        else:
            alpha = max(value, alpha)
            log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
        return value, "pass"

    for c in child:
        log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
        next_state = get_next_state(copy.deepcopy(state), c, player)
        temp_value = min_value(next_state, c, depth + 1, alpha, beta)[0]
        if value != max(value, temp_value):
            next_node = c
        value = max(value, temp_value)
        if value >= beta:
            log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
            return value, next_node
        else:
            alpha = max(value, alpha)
    log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
    return value, next_node


# min value
def min_value(state, node, depth, alpha, beta):
    if node == "pass" or node == "end":
        print_node = "pass"
    else:
        print_node = get_node(node)
    if depth >= cutOffDepth or node == "end":
        log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, evaluation(state), process(alpha), process(beta)))
        return evaluation(state), "end"
 #   if check_end(state):
  #      log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, evaluation(state), process(alpha), process(beta)))
  #      return evaluation(state), "end"
    value = p_inf
    child = get_valid_moves(state, opponent)
    if not child:
        log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
        # if both sides pass their move, the game is end
        if print_node == "pass":
            next_node = "end"
        else:
            next_node = "pass"
        value = min(value, max_value(copy.deepcopy(state), next_node, depth+1, alpha, beta)[0])
        if value <= alpha:
            log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
            return value, "pass"
        else:
            beta = min(value, beta)
            log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
        return value, "pass"
    for c in child:
        log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
        next_state = get_next_state(copy.deepcopy(state), c, opponent)
        temp_value = max_value(next_state, c, depth + 1, alpha, beta)[0]
        if value != temp_value:
            next_node = c
        value = min(value, temp_value)
        if value <= alpha:
            log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
            return value, next_node
        else:
            beta = min(value, beta)
    log.append("{0},{1},{2},{3},{4}\n".format(print_node, depth, process(value), process(alpha), process(beta)))
    return value, next_node


#  Alpha_beta_search
def alpha_beta_search(state):
    value, next_node = max_value(state, "root", 0, n_inf, p_inf)
    return value, next_node

# main
if __name__ == "__main__":
    log.append("Node,Depth,Value,Alpha,Beta\n")
    value, next_node = alpha_beta_search(copy.deepcopy(init_state))
    if next_node == "pass" or next_node == "end":
        next_state = copy.deepcopy(init_state)
    else:
        next_state = get_next_state(copy.deepcopy(init_state), next_node, player)

    with open("output.txt", "w")as outfile:
        for state in next_state:
            for i in state:
                outfile.write(i)
            outfile.write("\n")
        for l in log:
           outfile.write(str(l))
