import copy
from board import MoveResult

def best_move(board, current_player):
    legal_moves = get_legal_moves(board)
    best = None
    if current_player == 'X':
        best_score = float('-inf')
    else:
        best_score = float('inf')

    for move in legal_moves:
        new_board = copy.deepcopy(board)
        new_board.make_move(current_player, move)
        if current_player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        score = minimax_score(new_board, opponent)
            
        if current_player == 'X' and score > best_score:
            best_score = score
            best = move
        elif current_player == 'O' and score < best_score:
            best_score = score
            best = move

    return best

def minimax_score(board, current_player):
    if board.get_winner() == 'X':
        return 10
    elif board.get_winner() == 'O':
        return -10
    elif board.has_draw():
        return 0

    legal_moves = get_legal_moves(board)

    scores = []
    for move in legal_moves:
        new_board = copy.deepcopy(board)
        new_board.make_move(current_player, move)

        if current_player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        scores.append(minimax_score(new_board, opponent))

    if current_player == 'X':
        return max(scores)
    else:
        return min(scores)

def get_legal_moves(board):
    legal_moves = []
    for j in range(3):
        for i in range(3):
            if board.is_legal_move([i, j]) == MoveResult.CONTINUE:
                legal_moves.append([i,j])
    return legal_moves

