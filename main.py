import tkinter as tk
from board import Board, MoveResult
from minimax import get_legal_moves
import torch
from network import TicTacToeNet
from train import encode_board

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = Board()
        self.buttons = [[None] * 3 for _ in range(3)]
        self.human = None
        self.ai = None
        self.player = "X"

        self.net = TicTacToeNet()
        self.net.load_state_dict(torch.load("ttt_net.pth"))
        self.net.eval()  # disables dropout/batchnorm if you ever add them

        self.show_start_screen()

    def show_start_screen(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.grid(row=0, column=0)
        tk.Label(self.start_frame, text="Play as:", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.start_frame, text="X (Go First)", font=("Arial", 14), width=12,
                  command=lambda: self.start_game(human="X")).pack(pady=5)
        tk.Button(self.start_frame, text="O (Go Second)", font=("Arial", 14), width=12,
                  command=lambda: self.start_game(human="O")).pack(pady=5)

    def start_game(self, human):
        self.human = human
        if human == "X":
            self.ai = "O"
        else:
            self.ai = "X"

        self.start_frame.destroy()
        self.build_board()
        if self.player != self.human:
            self.status.config(text="AI is thinking...")
            self.root.after(300, self.ai_move)
        else:
            self.status.config(text=f"Your turn ({self.human})")

    def build_board(self):
        for j in range(3):
            for i in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 32), width=4, height=2,
                                command=lambda x=i, y=j: self.human_move(x, y))
                btn.grid(row=j, column=i)
                self.buttons[j][i] = btn
        self.status = tk.Label(self.root, font=("Arial", 14))
        self.status.grid(row=3, column=0, columnspan=3)

    def human_move(self, x, y):
        if self.player != self.human:
            return
        result = self.board.make_move(self.human, [x, y])
        if result == MoveResult.INVALID_LOC:
            return
        self.buttons[y][x].config(text=self.human)
        if self.check_end(result):
            return
        self.player = self.ai
        self.status.config(text="AI is thinking...")
        self.root.after(300, self.ai_move)

    def nn_move(self, board, current_player, net):
        from minimax import get_legal_moves
        state = encode_board(board, current_player)
        legal = get_legal_moves(board)
        legal_indices = [m[1] * 3 + m[0] for m in legal]

        with torch.no_grad():
            logits, _ = net(state)
            mask = torch.full((9,), float('-inf'))
            mask[legal_indices] = 0.0
            probs = torch.softmax(logits + mask, dim=0)

        idx = torch.argmax(probs).item()
        return [idx % 3, idx // 3]

    def ai_move(self):
        move = self.nn_move(self.board, self.ai, self.net)
        result = self.board.make_move(self.ai, move)
        self.buttons[move[1]][move[0]].config(text=self.ai)
        if self.check_end(result):
            return
        self.player = self.human
        self.status.config(text=f"Your turn ({self.human})")

    def check_end(self, result):
        if result == MoveResult.WIN:
            self.status.config(text=f"Player {self.board.get_winner()} Wins!")
            self.disable_board()
            self.show_reset_button()
            return True
        elif result == MoveResult.DRAW:
            self.status.config(text="It's a Draw!")
            self.disable_board()
            self.show_reset_button()
            return True
        return False

    def show_reset_button(self):
        tk.Button(self.root, text="Play Again", font=("Arial", 14),
                command=self.reset).grid(row=4, column=0, columnspan=3, pady=10)

    def reset(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.board = Board()
        self.board.reset()
        self.buttons = [[None]*3 for _ in range(3)]
        self.player = "X"
        self.human = None
        self.ai = None
        self.show_start_screen()

    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

root = tk.Tk()
TicTacToeGUI(root)
root.mainloop()
