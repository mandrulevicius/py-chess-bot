"""Analyze chess moves for sound effect purposes."""

import chess
from typing import Dict, Any


def analyze_move(board: chess.Board, move: chess.Move) -> Dict[str, Any]:
    """
    Analyze a chess move to determine its characteristics for sound effects.
    
    Args:
        board: Chess board before the move
        move: Chess move object
        
    Returns:
        Dict with move characteristics:
            - is_capture: Whether the move captures a piece
            - is_check: Whether the move puts opponent in check
            - is_checkmate: Whether the move is checkmate
            - is_castle: Whether the move is castling
            - is_promotion: Whether the move promotes a pawn
            - is_en_passant: Whether the move is en passant capture
    """
    # Make a copy to analyze the result
    temp_board = board.copy()
    
    # Check if move captures before making it
    is_capture = board.is_capture(move)
    is_en_passant = board.is_en_passant(move)
    is_castle = board.is_castling(move)
    is_promotion = move.promotion is not None
    
    # Make the move to check for check/checkmate
    temp_board.push(move)
    
    is_check = temp_board.is_check()
    is_checkmate = temp_board.is_checkmate()
    
    return {
        'is_capture': is_capture,
        'is_check': is_check,
        'is_checkmate': is_checkmate,
        'is_castle': is_castle,
        'is_promotion': is_promotion,
        'is_en_passant': is_en_passant
    }


def analyze_move_from_san(board: chess.Board, san_move: str) -> Dict[str, Any]:
    """
    Analyze a chess move from SAN notation.
    
    Args:
        board: Chess board before the move
        san_move: Move in Standard Algebraic Notation
        
    Returns:
        Dict with move characteristics (same as analyze_move)
    """
    try:
        move = board.parse_san(san_move)
        return analyze_move(board, move)
    except (chess.IllegalMoveError, chess.InvalidMoveError, ValueError):
        # Return all False if move is invalid
        return {
            'is_capture': False,
            'is_check': False,
            'is_checkmate': False,
            'is_castle': False,
            'is_promotion': False,
            'is_en_passant': False
        }