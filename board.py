from enum import Enum


class MoveResult(Enum):
    """Move result codes"""

    INVALID_LOC = "invalid_loc"
    INVALID_PLAYER = "invalid_player"
    CONTINUE = "continue"
    WIN = "win"
    DRAW = "draw"


class Board:
    """Tic-tac-toe board"""

    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.winner = None

    def get_board(self):
        return self.board

    def print_board(self):
        print("     0     1     2")
        for i, row in enumerate(self.board):
            print(i, row)

    def make_move(self, player, loc):
        """Makes a move on the board

        Args:
            player (char): the player making the move
            loc ([int, int]): the [x,y] location of the move being made

        Returns:
            result (MoveResult): result code of the move

        """
        if player not in ["X", "O"]:
            return MoveResult.INVALID_PLAYER

        legal = self.is_legal_move(loc)

        if legal != MoveResult.CONTINUE:
            return legal

        self.board[loc[1]][loc[0]] = player

        if self.has_win(player):
            return MoveResult.WIN
        elif self.has_draw():
            return MoveResult.DRAW
        else:
            return MoveResult.CONTINUE

    def is_legal_move(self, loc):
        """Checks if a move is legal

        Args:
            loc ([int, int]): the [x,y] location of the move

        Returns:
            result (MoveResult): result code of the move

        """
        if loc[0] < 0 or loc[0] > 2:
            return MoveResult.INVALID_LOC
        if loc[1] < 0 or loc[1] > 2:
            return MoveResult.INVALID_LOC

        if self.board[loc[1]][loc[0]] is not None:
            return MoveResult.INVALID_LOC

        return MoveResult.CONTINUE

    def has_win(self, player):
        """Makes a move on the board

        Args:
            player (char): the player making the move

        Returns:
            result (bool): True if the player has a win, False otherwise

        """
        for j in range(3):
            if self.board[j][0] is None:
                continue
            if (
                self.board[j][0] == self.board[j][1]
                and self.board[j][1] == self.board[j][2]
            ):
                self.winner = player
                return True

        for i in range(3):
            if self.board[0][i] is None:
                continue
            if (
                self.board[0][i] == self.board[1][i]
                and self.board[1][i] == self.board[2][i]
            ):
                self.winner = player
                return True

        if self.board[0][0] is not None:
            if (
                self.board[0][0] == self.board[1][1]
                and self.board[1][1] == self.board[2][2]
            ):
                self.winner = player
                return True

        if self.board[0][2] is not None:
            if (
                self.board[0][2] == self.board[1][1]
                and self.board[1][1] == self.board[2][0]
            ):
                self.winner = player
                return True

        return False

    def reset(self):
        """Resets the board"""
        self.board = [[None] * 3 for _ in range(3)]

    def get_winner(self):
        return self.winner

    def has_draw(self):
        """Makes a move on the board
        Returns:
            result (bool): True if there is a tie on the board, False otherwise

        """
        for row in self.board:
            for item in row:
                if item is None:
                    return False
        return True
