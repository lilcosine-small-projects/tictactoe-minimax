from board import Board, MoveResult
from minimax import best_move

board = Board()

player = "X"
result = MoveResult.CONTINUE
while True:
    board.print_board()
    if player == 'X':
        move = best_move(board, "X")
        result = board.make_move("X", move)
    else:
        x = int(input("X Location: "))
        y = int(input("Y Location: "))
        result = board.make_move(player, [x, y])
        while result == MoveResult.INVALID_LOC:
            print("Invalid Move! Please enter a valid move!")
            x = int(input("X Location: "))
            y = int(input("Y Location: "))
            result = board.make_move(player, [x, y])
    if result == MoveResult.WIN:
        board.print_board()
        print(f"Player {player} Wins!")
        break
    elif result == MoveResult.DRAW:
        board.print_board()
        print("You Tied!")
        break
    if player == "X":
        player = "O"
    else:
        player = "X"
