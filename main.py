from board import Board, MoveResult

board = Board()

player = "X"
result = MoveResult.CONTINUE
while True:
    board.print_board()
    x = int(input("X Location: "))
    y = int(input("Y Location: "))
    result = board.make_move(player, [x, y])
    while result == MoveResult.INVALID_LOC:
        print("Invalid Move! Please enter a valid move!")
        x = int(input("X Location: "))
        y = int(input("Y Location: "))
        result = board.make_move(player, [x, y])
    if result == MoveResult.WIN:
        print(f"Player {player} Wins!")
        break
    elif result == MoveResult.DRAW:
        print("You Tied!")
        break
    if player == "X":
        player = "O"
    else:
        player = "X"
