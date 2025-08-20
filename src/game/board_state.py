"""Chess board state management."""

import chess
from .move_validator import validate_move


def create_board(fen=None):
    """
    Create a chess board.
    
    Args:
        fen (str, optional): FEN string for custom position.
                           If None, creates starting position.
    
    Returns:
        chess.Board: Chess board object
    """
    if fen is None:
        return chess.Board()
    else:
        return chess.Board(fen)


def get_board_fen(board):
    """
    Get FEN string representation of board.
    
    Args:
        board (chess.Board): Chess board object
    
    Returns:
        str: FEN string of current position
    """
    return board.fen()


def apply_move(board, san_move):
    """
    Apply a move to the board (immutable - returns new board).
    
    Args:
        board (chess.Board): Current board state
        san_move (str): Move in SAN notation
    
    Returns:
        dict: Result with keys:
            - success: True if move was applied successfully
            - new_board: New board state (if successful)
            - error: Error message (if unsuccessful)
    """
    # Validate the move first
    current_fen = get_board_fen(board)
    validation_result = validate_move(san_move, current_fen)
    
    if not validation_result["valid"]:
        return {
            "success": False,
            "error": validation_result["error"]
        }
    
    if not validation_result.get("legal", True):
        return {
            "success": False,
            "error": validation_result["error"]
        }
    
    # Create a copy of the board and apply the move
    try:
        new_board = board.copy()
        move_object = validation_result["move_object"]
        new_board.push(move_object)
        
        return {
            "success": True,
            "new_board": new_board
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to apply move: {str(e)}"
        }


def get_legal_moves(board):
    """
    Get list of legal moves in SAN notation from current position.
    
    Args:
        board (chess.Board): Chess board object
    
    Returns:
        list: List of legal moves in SAN notation
    """
    return [board.san(move) for move in board.legal_moves]