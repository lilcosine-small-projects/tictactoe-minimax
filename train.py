import math
import copy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from network import TicTacToeNet
from board import Board, MoveResult
from minimax import get_legal_moves


def encode_board(board, current_player):
    """Encode board as float tensor from current player's perspective."""
    flat = []
    for row in board.get_board():
        for cell in row:
            if cell is None:
                flat.append(0.0)
            elif cell == current_player:
                flat.append(1.0)
            else:
                flat.append(-1.0)
    return torch.tensor(flat, dtype=torch.float32)


def was_blocking_move(board, move, opponent):
    """Check if the move just played blocked the opponent from winning."""
    test_board = copy.deepcopy(board)
    # Undo the move by setting cell back to None
    test_board.get_board()[move[1]][move[0]] = None
    # Check if the opponent could have won there
    test_board.get_board()[move[1]][move[0]] = opponent
    return test_board.has_win(opponent)


def has_winning_threat(board, player):
    """Check if player has any move that would win immediately."""
    for move in get_legal_moves(board):
        test_board = copy.deepcopy(board)
        result = test_board.make_move(player, move)
        if result == MoveResult.WIN:
            return True
    return False


def get_reward(result, board, move, player):
    """Shaped reward: win, draw, block, or neutral."""
    if result == MoveResult.WIN:
        return 1.0
    if result == MoveResult.DRAW:
        return 0.3
    opponent = "O" if player == "X" else "X"
    if was_blocking_move(board, move, opponent):
        return 0.5
    return 0.0


def play_game(net, epsilon=0.1, random_opponent_prob=0.3):
    """
    Play one game of self-play.
    Returns a list of (state_tensor, action, player, reward) tuples + winner.
    Occasionally uses a random opponent to increase diversity.
    """
    board = Board()
    history = []
    current = "X"
    learning_player = "X"

    while True:
        state = encode_board(board, current)
        legal = get_legal_moves(board)
        legal_indices = [m[1] * 3 + m[0] for m in legal]

        use_random = (
            current != learning_player and
            torch.rand(1).item() < random_opponent_prob
        )

        if use_random:
            idx = legal_indices[torch.randint(len(legal_indices), (1,)).item()]
        else:
            logits, _ = net(state)
            mask = torch.full((9,), float('-inf'))
            mask[legal_indices] = 0.0
            probs = torch.softmax(logits + mask, dim=0)

            if torch.rand(1).item() < epsilon:
                idx = legal_indices[torch.randint(len(legal_indices), (1,)).item()]
            else:
                idx = torch.multinomial(probs, 1).item()

        move = [idx % 3, idx // 3]
        result = board.make_move(current, move)
        reward = get_reward(result, board, move, current)

        history.append((state, idx, current, reward))

        if result == MoveResult.WIN:
            return history, current
        elif result == MoveResult.DRAW:
            return history, None

        current = "O" if current == "X" else "X"


def train_step(net, optimizer, history, winner):
    """Update the network based on one completed game."""
    optimizer.zero_grad()
    total_loss = torch.tensor(0.0, requires_grad=True)

    for state, action, player, shaped_reward in history:
        # Final outcome reward from this player's perspective
        if winner is None:
            outcome = 0.3   # draw
        elif winner == player:
            outcome = 1.0
        else:
            outcome = -1.0

        # Blend shaped reward with final outcome
        reward = 0.6 * outcome + 0.4 * shaped_reward

        logits, value = net(state)
        probs = torch.softmax(logits, dim=0)
        log_prob = torch.log(probs[action] + 1e-8)

        advantage = reward - value.squeeze().detach()

        policy_loss = -log_prob * advantage
        value_loss = F.mse_loss(value.squeeze(), torch.tensor(reward))

        total_loss = total_loss + policy_loss + 0.5 * value_loss

    total_loss.backward()
    optimizer.step()


def train(episodes=200_000):
    net = TicTacToeNet()
    optimizer = optim.Adam(net.parameters(), lr=1e-3)

    for ep in range(episodes):
        # Slower epsilon decay with a higher floor
        epsilon = max(0.1, 1.0 - ep / (episodes * 0.9))

        history, winner = play_game(net, epsilon=epsilon)
        train_step(net, optimizer, history, winner)

        if ep % 5000 == 0:
            print(f"Episode {ep}/{episodes}, epsilon={epsilon:.3f}")

    torch.save(net.state_dict(), "ttt_net.pth")
    print("Training complete. Model saved to ttt_net.pth")
    return net


if __name__ == "__main__":
    train()
