import math

alpha = -math.inf
beta = math.inf

# moves can be made only on EMPTY tiles
def valid_moves(board):
    return all([])

# check for terminal state
def terminal(board):
    return not valid_moves(board)

# evaluate child nodes
def evaluate(board):
    return

# apply move made by the respective player
def apply(board, move):
    board[move[0]][move[1]] = 1

# choose the move with the highest value
def best_move(board):
    best_value = -math.inf
    for move in valid_moves(board):
        score = minimise(apply(board, move, 'X'), alpha, beta)
        if score > best_value:
            best_value = score
        alpha = max(alpha, best_value)
    return best_value

# player MAX
def maximise(board, alpha, beta):
    if terminal(board):
        return evaluate(board)

    v = -math.inf
    for move in valid_moves(board):
        v = max(v, minimise(apply(board, move, 'X'), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

# player MIN
def minimise(board, alpha, beta):
    if terminal(board):
        return evaluate(board)

    v = math.inf
    for move in valid_moves(board):
        v = min(v, maximise(apply(board, move, 'O'), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
