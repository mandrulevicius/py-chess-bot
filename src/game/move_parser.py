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
            - capture: True if move is a capture
            - check: True if move gives check
            - checkmate: True if move is checkmate
            - castling: "kingside" or "queenside" for castling
            - promotion: promoted piece type
    """
    if not san_notation or not isinstance(san_notation, str):
        return {"valid": False, "error": "Invalid input"}
    
    san_notation = san_notation.strip()
    if not san_notation:
        return {"valid": False, "error": "Empty notation"}
    
    # Initialize result dictionary
    result = {"valid": True}
    
    # Remove check/checkmate symbols and store them
    if san_notation.endswith('#'):
        result["checkmate"] = True
        san_notation = san_notation[:-1]
    elif san_notation.endswith('+'):
        result["check"] = True
        san_notation = san_notation[:-1]
    
    # Handle castling
    if san_notation == "O-O":
        result["castling"] = "kingside"
        return result
    elif san_notation == "O-O-O":
        result["castling"] = "queenside"
        return result
    
    # Handle pawn promotion
    promotion_match = re.search(r'=([QRBN])$', san_notation)
    if promotion_match:
        piece_names = {'Q': 'queen', 'R': 'rook', 'B': 'bishop', 'N': 'knight'}
        result["promotion"] = piece_names[promotion_match.group(1)]
        san_notation = san_notation[:promotion_match.start()]
    
    # Check for capture
    if 'x' in san_notation:
        result["capture"] = True
        parts = san_notation.split('x')
        if len(parts) != 2:
            return {"valid": False, "error": f"Invalid capture notation: {san_notation}x"}
        piece_part, destination = parts
    else:
        piece_part = san_notation[:-2] if len(san_notation) > 2 else ""
        destination = san_notation[-2:]
    
    # Validate destination square
    if not re.match(r'^[a-h][1-8]$', destination):
        return {"valid": False, "error": f"Invalid destination square: {destination}"}
    
    result["destination"] = destination
    
    # Determine piece type
    if not piece_part:  # Simple pawn move
        result["piece"] = "pawn"
    elif piece_part in ['K', 'Q', 'R', 'B', 'N']:  # Simple piece move
        piece_names = {'K': 'king', 'Q': 'queen', 'R': 'rook', 'B': 'bishop', 'N': 'knight'}
        result["piece"] = piece_names[piece_part]
    elif len(piece_part) == 1 and piece_part in 'abcdefgh':  # Pawn capture (e.g., "e" in "exd5")
        result["piece"] = "pawn"
    else:
        return {"valid": False, "error": f"Invalid piece notation: {piece_part}"}
    
    return result