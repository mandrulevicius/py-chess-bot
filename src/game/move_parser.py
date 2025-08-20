"""Move parsing functionality for chess notation."""

import re


def parse_san_move(san_notation):
    """
    Parse Standard Algebraic Notation move string.
    
    Args:
        san_notation (str): Move in SAN format (e.g., "e4", "Nf3", "O-O")
    
    Returns:
        dict: Parsed move information with keys:
            - piece: piece type
            - destination: target square  
            - valid: whether the notation is valid
            - error: error message if invalid
    """
    if not san_notation or not isinstance(san_notation, str):
        return {"valid": False, "error": "Invalid input"}
    
    san_notation = san_notation.strip()
    
    # Basic pawn moves (e4, d5, etc.)
    pawn_pattern = r'^[a-h][1-8]$'
    if re.match(pawn_pattern, san_notation):
        return {
            "piece": "pawn",
            "destination": san_notation,
            "valid": True
        }
    
    # Piece moves (Nf3, Be5, etc.)
    piece_pattern = r'^([KQRBN])[a-h][1-8]$'
    piece_match = re.match(piece_pattern, san_notation)
    if piece_match:
        piece_char = piece_match.group(1)
        piece_names = {
            'K': 'king',
            'Q': 'queen', 
            'R': 'rook',
            'B': 'bishop',
            'N': 'knight'
        }
        return {
            "piece": piece_names[piece_char],
            "destination": san_notation[1:],
            "valid": True
        }
    
    # If we get here, notation is invalid
    return {
        "valid": False,
        "error": f"Invalid chess notation: {san_notation}"
    }