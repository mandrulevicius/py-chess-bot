"""Move validation with board position awareness."""

import chess
from .move_parser import parse_san_move


def validate_move(san_notation, board_state=None):
    """
    Validate a move with optional board position checking.
    
    Args:
        san_notation (str): Move in SAN format
        board_state (str, optional): FEN string representing board position
    
    Returns:
        dict: Validation result with keys:
            - All keys from parse_san_move()
            - legal: True if move is legal in given position (if board_state provided)
            - move_object: python-chess Move object (if legal and board_state provided)
    """
    # Step 1: Parse notation syntax
    result = parse_san_move(san_notation)
    
    if not result["valid"]:
        return result
    
    # Step 2: If no board state provided, return syntax validation only
    if board_state is None:
        return result
    
    # Step 3: Validate move legality with python-chess
    try:
        board = chess.Board(board_state)
        move = board.parse_san(san_notation)
        
        # Move is legal
        result["legal"] = True
        result["move_object"] = move
        
    except ValueError:
        # Move syntax is valid but not legal in current position
        result["legal"] = False
        result["error"] = f"Move '{san_notation}' is not legal in current position"
    
    except Exception as e:
        # Something else went wrong (invalid FEN, etc.)
        result["legal"] = False
        result["error"] = f"Board validation error: {str(e)}"
    
    return result