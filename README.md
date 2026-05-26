# Tic-Tac-Toe Neural Net

Experimental branch to play against a neural net trained with self-play

A desktop implementation of Tic-tac-toe built with Python and Tkinter, featuring an AI opponent driven by the Minimax algorithm. The AI performs an exhaustive search of the game tree to determine the optimal move at every turn, guaranteeing play that cannot be outperformed — the strongest result a human player can achieve is a draw.

---

## Features

- **Zero-dependency GUI** built entirely on Python's standard-library Tkinter
- **Optimal AI opponent** via full-depth Minimax search with no pruning
- **Side selection** — the player chooses to play as X (first move) or O (second move) at the start of each session
- **Session reset** — a full state reset is performed between games without restarting the application

---

## Project Structure

```
.
├── main.py        # Presentation layer — GUI construction and user interaction (Tkinter)
├── board.py       # Domain layer — board state, move validation, and terminal condition detection
└── minimax.py     # AI layer — Minimax algorithm and move selection
```

### `board.py`
Defines the `Board` class, which encapsulates the 3×3 game grid. Responsibilities include move validation, win detection across all rows, columns, and diagonals, draw detection, and the `MoveResult` enum used as a structured return type throughout the codebase.

### `minimax.py`
Contains the Minimax implementation. `best_move()` serves as the public entry point, iterating over all legal moves and returning the one with the optimal score. `minimax_score()` recursively traverses the full game tree, assigning scores to terminal states and propagating values upward via maximisation (X) and minimisation (O).

### `main.py`
Implements the application's presentation layer via the `TicTacToeGUI` class. Manages the start screen, board rendering, human input handling, AI move dispatch with a short delay for responsiveness, and end-of-game state presentation.

---

## Requirements

- Python 3.x
- Tkinter (included in the Python standard library)

> On some Linux distributions, Tkinter must be installed separately:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## Getting Started

1. **Clone the repository**
   ```bash
   git https://github.com/lilcosine-small-projects/tictactoe-minimax.git
   cd tictactoe-minimax
   ```

2. **Launch the application**
   ```bash
   python main.py
   ```

No virtual environment or additional package installation is required.

---

## Usage

1. On launch, select a side — **X** moves first, **O** moves second
2. Click any unoccupied cell to place your mark
3. The AI responds automatically following each player move
4. At the conclusion of a game, select **Play Again** to begin a new session

---

## AI Implementation

The AI is driven by the **Minimax algorithm**, a recursive decision-making strategy for two-player zero-sum games. At each turn, the algorithm enumerates all legal moves, simulates every resulting game tree to its terminal state, and selects the move that yields the optimal outcome under the assumption that both players act rationally.

Terminal states are scored as follows:

| Outcome | Score |
|---------|-------|
| X wins  | +10   |
| O wins  | −10   |
| Draw    |  0    |

X acts as the maximising player; O acts as the minimising player. Because the search is exhaustive and Tic-tac-toe's game tree is finite and fully enumerable, the algorithm always identifies the provably optimal move for the active player.
