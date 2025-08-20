"""Basic chess game loop functionality."""

from .board_state import create_board, apply_move, get_board_fen, get_legal_moves as get_board_legal_moves


def create_game(position=None):
    """
    Create a new chess game.
    
    Args:
        position (str, optional): FEN string for custom starting position
    
    Returns:
        dict: Game state with keys:
            - board: chess board object
            - move_history: list of moves made
            - turn_count: current turn number
    """
    board = create_board(position)
    
    return {
        "board": board,
        "move_history": [],
        "turn_count": 1 if position is None else _get_turn_from_fen(position)
    }


def get_current_player(game):
    """
    Get the current player to move.
    
    Args:
        game (dict): Game state
    
    Returns:
        str: "white" or "black"
    """
    return "white" if game["board"].turn else "black"


def get_game_status(game):
    """
    Get current game status.
    
    Args:
        game (dict): Game state
    
    Returns:
        dict: Status with keys:
            - active: True if game is ongoing
            - winner: "white", "black", or None
            - turn_count: current turn number
            - result: game result description
    """
    board = game["board"]
    
    if board.is_checkmate():
        winner = "black" if board.turn else "white"  # Opposite of current player
        return {
            "active": False,
            "winner": winner,
            "turn_count": game["turn_count"],
            "result": f"{winner.capitalize()} wins by checkmate"
        }
    elif board.is_stalemate():
        return {
            "active": False,
            "winner": None,
            "turn_count": game["turn_count"],
            "result": "Draw by stalemate"
        }
    elif board.is_insufficient_material():
        return {
            "active": False,
            "winner": None,
            "turn_count": game["turn_count"],
            "result": "Draw by insufficient material"
        }
    else:
        return {
            "active": True,
            "winner": None,
            "turn_count": game["turn_count"],
            "result": "Game in progress"
        }


def make_move(game, san_move):
    """
    Make a move in the game (immutable - returns new game state).
    
    Args:
        game (dict): Current game state
        san_move (str): Move in SAN notation
    
    Returns:
        dict: Result with keys:
            - success: True if move was made successfully
            - new_game: New game state (if successful)
            - error: Error message (if unsuccessful)
    """
    # Apply move to board
    move_result = apply_move(game["board"], san_move)
    
    if not move_result["success"]:
        return {
            "success": False,
            "error": move_result["error"]
        }
    
    # Create new game state
    new_game = {
        "board": move_result["new_board"],
        "move_history": game["move_history"] + [san_move],
        "turn_count": game["turn_count"] + (1 if game["board"].turn else 0)  # Increment on white's move
    }
    
    return {
        "success": True,
        "new_game": new_game
    }


def get_legal_moves(game):
    """
    Get list of legal moves from current game position.
    
    Args:
        game (dict): Game state
    
    Returns:
        list: List of legal moves in SAN notation
    """
    return get_board_legal_moves(game["board"])


def get_move_history(game):
    """
    Get the move history for the game.
    
    Args:
        game (dict): Game state
    
    Returns:
        list: List of moves made in SAN notation
    """
    return game["move_history"].copy()


def _get_turn_from_fen(fen):
    """Extract turn number from FEN string."""
    if fen is None:
        return 1
    
    try:
        parts = fen.split()
        if len(parts) >= 6:
            return int(parts[5])
    except (ValueError, IndexError):
        pass
    
    return 1