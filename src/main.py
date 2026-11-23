import math, time, random

# node counter
nodes = 0

# list of line patterns to win the game
patterns = [
    [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)], # horizontal
    [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)], # vertical
    [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)] # diagonal
]

# moves can be made only on EMPTY tiles
def valid_moves(board):
    return [(r, c) for r in range (3) for c in range (3) if board[r][c] == 0]

# board that has valid cells
def valid_board(board):
    flat = [c for row in board for c in row]
    return flat.count(1) == flat.count(-1)

# check for terminal state
def terminal(board):
    return result(board) != 0 or not valid_moves(board)

# apply move made by the respective player
def apply(board, move, player):
    new_board = [row[:] for row in board]
    new_board[move[0]][move[1]] = 1 if player == 'X' else -1
    return new_board

# choose the move with the highest value
def best_move(board):
    best_value = -math.inf
    best = None
    alpha, beta = -math.inf, math.inf

    for move in valid_moves(board):
        score = minimise(apply(board, move, 'X'), alpha, beta)
        if score > best_value:
            best_value = score
            best = move
        alpha = max(alpha, best_value)
    return best_value, best

# player MAX
def maximise(board, alpha, beta):
    global nodes
    nodes += 1

    if terminal(board):
        return result(board)

    v = -math.inf
    for move in valid_moves(board):
        v = max(v, minimise(apply(board, move, 'X'), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

# player MIN
def minimise(board, alpha, beta):
    global nodes
    nodes += 1

    if terminal(board):
        return result(board)

    v = math.inf
    for move in valid_moves(board):
        v = min(v, maximise(apply(board, move, 'O'), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

# choose best move as baseline without pruning
def minimax(board):
    best_value = -math.inf
    best = None

    for move in valid_moves(board):
        score = min_plain(apply(board, move, 'X'))

        if score > best_value:
            best_value = score
            best = move
    return best_value, best

def max_plain(board):
    global nodes
    nodes += 1

    if terminal(board):
        return result(board)
    return max(min_plain(apply(board, m, 'X')) for m in valid_moves(board))

def min_plain(board):
    global nodes
    nodes += 1

    if terminal(board):
        return result(board)
    return min(max_plain(apply(board, m, 'O')) for m in valid_moves(board))

# determine game result upon reaching terminal state
def result(board):
    for line in patterns:
        total = sum(board[r][c] for r, c in line)

        if total == 3:
            return 1 # X wins
        if total == -3:
            return -1 # O wins
    return 0 # draw

# run case
def run_case(name, board):
    global nodes

    nodes = 0
    t = time.perf_counter()
    ab_val, ab_move = best_move(board)
    ab_time = (time.perf_counter() - t) * 1000
    ab_nodes = nodes

    nodes = 0
    t = time.perf_counter()
    mm_val, mm_move = minimax(board)
    mm_time = (time.perf_counter() - t) * 1000
    mm_nodes = nodes

    assert ab_val == mm_val, f"Value mismatch {name}"
    reduction = (mm_nodes - ab_nodes) / mm_nodes * 100
    print(f"{name:<22} | MM {mm_nodes:>7} {mm_time:>8.1f}ms | AB {ab_nodes:>6} {ab_time:>7.1f}ms | val {ab_val:>2} | move {ab_move} | -{reduction:.1f}%")

# randomize
def play_random():
    board = [[0]*3 for _ in range (3)]
    while not terminal(board):
        _, move = best_move(board)
        board = apply(board, move, 'X')
        if terminal(board):
            break
        board = apply(board, random.choice(valid_moves(board)), 'O')
    return result(board)

def agent_move(board, agent):
    if agent == 'O':
        board = [[-c for c in row] for row in board]
    _, move = best_move(board)
    return move

def play_perfect():
    board = [[0]*3 for _ in range (3)]
    player = 'X'
    while not terminal(board):
        board = apply(board, agent_move(board, player), player)
        player = 'O' if player == 'X' else 'X'
    return result(board)

# run if directly called
if __name__ == "__main__":
    results = {1: 0, 0: 0, -1: 0}
    for _ in range (200):
        results[play_random()] += 1
    print("Wins:", results[1], "Draws:", results[0], "Losses:", results[-1])

    cases = {
        "Empty": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "O center": [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
        "Win available": [[1, 1, 0], [-1, -1, 0], [0, 0, 0]],
        "Must block": [[-1, -1, 0], [0, 1, 0], [0, 0, 1]],
        "Close to full": [[1, -1, 1], [-1, 1, -1], [0, 0, 0]],
    }

    for name, b in cases.items():
        assert valid_board(b), f"Invalid board {name}"
        run_case(name, b)

print(play_perfect())