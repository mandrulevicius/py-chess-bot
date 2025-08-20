"""Console interface for human chess interaction."""

import os
import sys
from ..game.game_loop import get_current_player, get_game_status, get_legal_moves, get_move_history


def display_welcome():
    """Display welcome message and game instructions."""
    print("=" * 50)
    print("      Welcome to PyChessBot!")
    print("      Human vs AI Chess Game")
    print("=" * 50)
    print()
    print("Instructions:")
    print("- Enter moves in standard algebraic notation (e.g., e4, Nf3, O-O)")
    print("- Type 'help' for available commands")
    print("- Type 'quit' to exit the game")
    print()


def display_board(game):
    """
    Display current game position and status.
    
    Args:
        game (dict): Current game state
    """
    status = get_game_status(game)
    current_player = get_current_player(game)
    
    print(f"\nTurn {status['turn_count']}: {current_player.capitalize()} to move")
    print(f"Game Status: {status['result']}")
    
    # Display FEN for debugging (as specified in design - no ASCII board)
    from ..game.board_state import get_board_fen
    fen = get_board_fen(game["board"])
    print(f"Position: {fen}")
    print()


def get_user_move():
    """
    Get move input from user with input validation.
    
    Returns:
        str: User's move in SAN notation
    """
    while True:
        try:
            move = input("Enter your move: ").strip()
            if move:  # Non-empty after stripping
                return move
            print("Please enter a move.")
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted by user.")
            sys.exit(0)


def show_message(message):
    """
    Display a message to the user.
    
    Args:
        message (str): Message to display
    """
    print(message)


def show_error(error_message):
    """
    Display an error message with special formatting.
    
    Args:
        error_message (str): Error message to display
    """
    print(f"ERROR: {error_message}")


def show_move_history(game):
    """
    Display move history in chess notation.
    
    Args:
        game (dict): Current game state
    """
    history = get_move_history(game)
    
    if not history:
        print("No moves played yet.")
        return
    
    print("Move History:")
    
    # Display moves in pairs (white, black)
    for i in range(0, len(history), 2):
        move_number = (i // 2) + 1
        white_move = history[i]
        black_move = history[i + 1] if i + 1 < len(history) else ""
        
        if black_move:
            print(f"{move_number}. {white_move} {black_move}")
        else:
            print(f"{move_number}. {white_move}")
    print()


def show_game_status(game):
    """
    Display current game status.
    
    Args:
        game (dict): Current game state
    """
    status = get_game_status(game)
    print(f"Game Status: {status['result']}")
    
    if not status['active']:
        print("Game Over!")
        if status['winner']:
            print(f"Winner: {status['winner'].capitalize()}")
    print()


def show_legal_moves(game):
    """
    Display available legal moves.
    
    Args:
        game (dict): Current game state
    """
    legal_moves = get_legal_moves(game)
    
    if not legal_moves:
        print("No legal moves available.")
        return
    
    print("Legal moves:", end=" ")
    
    # Display moves in a readable format
    moves_per_line = 10
    for i, move in enumerate(legal_moves):
        if i > 0 and i % moves_per_line == 0:
            print()  # New line every 10 moves
            print("             ", end=" ")  # Indent continuation
        print(move, end=" ")
    
    print()  # Final newline
    print()


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_help():
    """Display help information."""
    print("Available commands:")
    print("  help     - Show this help message")
    print("  history  - Show move history")
    print("  legal    - Show legal moves")
    print("  status   - Show game status")
    print("  clear    - Clear screen")
    print("  quit     - Exit game")
    print()
    print("Chess notation examples:")
    print("  e4       - Pawn to e4")
    print("  Nf3      - Knight to f3")
    print("  Bxc5     - Bishop captures on c5")
    print("  O-O      - Kingside castling")
    print("  O-O-O    - Queenside castling")
    print("  e8=Q     - Pawn promotion to Queen")
    print()