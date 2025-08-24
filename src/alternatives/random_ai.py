"""Random chess AI - basic implementation for testing and fallback."""

import random
import time
from typing import Any, Dict, Optional
from ..core.interfaces import ChessAI


class RandomChessAI(ChessAI):
    """
    Random move AI for testing and fallback purposes.
    
    This AI makes random legal moves and provides basic position evaluation.
    Useful for testing the pluggable architecture without requiring Stockfish.
    """
    
    def __init__(self):
        self.difficulty = 1
        self.initialized = False
        self.move_count = 0
    
    def initialize(self, difficulty: int = 8, **kwargs) -> bool:
        """Initialize the random AI."""
        self.difficulty = max(1, min(10, difficulty))  # Clamp to reasonable range
        self.initialized = True
        return True
    
    def get_best_move(self, board_state: Any, time_limit: float = 3.0) -> Optional[str]:
        """
        Get a random legal move.
        """
        if not self.initialized:
            return None
        
        # Get legal moves (this would need to be integrated with actual board state)
        # For now, return some common opening moves
        opening_moves = [
            'e4', 'e3', 'd4', 'd3', 'Nf3', 'Nc3', 'c4', 'f4', 'g3', 'b3'
        ]
        
        middlegame_moves = [
            'Nxe5', 'Bxf7+', 'Qh5', 'Rd1', 'O-O', 'h3', 'a3', 'Re1'
        ]
        
        # Choose move set based on game progress
        if self.move_count < 10:
            available_moves = opening_moves
        else:
            available_moves = middlegame_moves
        
        self.move_count += 1
        return random.choice(available_moves)
    
    def evaluate_position(self, board_state: Any) -> Dict[str, Any]:
        """
        Random position evaluation for testing.
        """
        if not self.initialized:
            return {
                'evaluation_type': 'error',
                'error': 'AI not initialized'
            }
        
        # Generate random evaluation
        score = random.randint(-300, 300)  # Random centipawn evaluation
        
        return {
            'score': score,
            'evaluation_type': 'cp',
            'confidence': 'low',
            'note': 'Random evaluation for testing'
        }
    
    def cleanup(self) -> None:
        """Clean up AI resources (no-op for random AI)."""
        self.initialized = False


# Register with factory
from ..core.interfaces import ComponentFactory
ComponentFactory.register_ai('random', RandomChessAI)