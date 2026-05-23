from enum import Enum

class MoveResult(Enum):
    INVALID_LOC = "invalid_loc"
    INVALID_PLAYER = "invalid_player"
    CONTINUE = "continue"
    WIN = "win"
    DRAW = "draw"


class Board():
    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]

    def get_board(self):
        return self.board

    def print_board(self):
        print("     0     1     2")
        for i, row in enumerate(self.board):
            print(i, row)

    def make_move(self, player, loc):
        if loc[0] < 0 or loc[0] > 2:
            return MoveResult.INVALID_LOC
        if loc[1] < 0 or loc[1] > 2:
            return MoveResult.INVALID_LOC
        if player not in ["X", "O"]:
            return MoveResult.INVALID_PLAYER

        if self.board[loc[1]][loc[0]] != None:
            return MoveResult.INVALID_LOC

        self.board[loc[1]][loc[0]] = player

        if self.has_win():
            return MoveResult.WIN
        elif self.has_draw():
            return MoveResult.DRAW
        else:
            return MoveResult.CONTINUE

    def has_win(self):
        for j in range(3):
            if self.board[j][0] == None:
                continue
            if self.board[j][0] == self.board[j][1] and self.board[j][1] == self.board[j][2]:
                return True

        for i in range(3):
            if self.board[0][i] == None:
                continue
            if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]:
                return True

        if self.board[0][0] != None:
            if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
                return True
        
        if self.board[0][2] != None:
            if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
                return True
        
        return False

    def reset(self):
        self.board = [[None] * 3 for _ in range(3)]

    def has_draw(self):
        for row in self.board:
            for item in row:
                if item == None:
                    return False
        return True

