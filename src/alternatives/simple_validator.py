"""Simple chess move validator - basic implementation without external dependencies."""

import re
from typing import Any, Dict, List
from ..core.interfaces import ChessMoveValidator


class SimpleChessValidator(ChessMoveValidator):
    """
    Basic chess move validator with essential rules.
    
    This is a simplified implementation that covers basic moves
    but may not handle all edge cases like en passant, castling rights, etc.
    """
    
    def __init__(self):
        self.piece_symbols = {
            'K': 'king', 'Q': 'queen', 'R': 'rook', 
            'B': 'bishop', 'N': 'knight', 'P': 'pawn'
        }
    
    def validate_move(self, board_state: Any, move: str) -> Dict[str, Any]:
        """
        Basic move validation.
        
        Note: This is a simplified validator for demonstration purposes.
        It performs basic syntax checking but not full chess rule validation.
        """
        try:
            # Basic move format validation
            move = move.strip()
            
            if not move:
                return {'valid': False, 'error': 'Empty move'}
            
            # Handle special moves
            if move in ['O-O', '0-0', 'O-O-O', '0-0-0']:
                return {'valid': True, 'move_type': 'castle'}
            
            # Basic algebraic notation pattern
            # Matches moves like e4, Nf3, Bxc5, etc.
            pattern = r'^[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?$'
            
            if re.match(pattern, move):
                return {'valid': True, 'move_type': 'normal'}
            else:
                return {'valid': False, 'error': f'Invalid move format: {move}'}
                
        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}
    
    def get_legal_moves(self, board_state: Any) -> List[str]:
        """
        Get legal moves (simplified implementation).
        
        Returns a basic set of moves for demonstration.
        In a real implementation, this would analyze the board position.
        """
        # This is a placeholder implementation
        # In reality, you'd need to analyze the current board position
        basic_moves = [
            'e4', 'e3', 'd4', 'd3', 'Nf3', 'Nc3', 'Nge2', 'Be2', 'Bd3', 'Bc4'
        ]
        return basic_moves


# Register with factory
from ..core.interfaces import ComponentFactory
ComponentFactory.register_validator('simple', SimpleChessValidator)