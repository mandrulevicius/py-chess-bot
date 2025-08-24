"""Core interfaces for pluggable architecture."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class ChessMoveValidator(ABC):
    """Interface for chess move validation."""
    
    @abstractmethod
    def validate_move(self, board_state: Any, move: str) -> Dict[str, Any]:
        """
        Validate a chess move.
        
        Args:
            board_state: Current board state
            move: Move in algebraic notation
            
        Returns:
            Dict with 'valid': bool and optional 'error': str
        """
        pass
    
    @abstractmethod
    def get_legal_moves(self, board_state: Any) -> List[str]:
        """Get list of legal moves in current position."""
        pass


class ChessBoardState(ABC):
    """Interface for chess board state management."""
    
    @abstractmethod
    def create_initial_board(self) -> Any:
        """Create initial chess board position."""
        pass
    
    @abstractmethod
    def make_move(self, board: Any, move: str) -> Tuple[Any, Dict[str, Any]]:
        """
        Make a move and return new board state.
        
        Returns:
            Tuple of (new_board, move_info)
        """
        pass
    
    @abstractmethod
    def get_board_fen(self, board: Any) -> str:
        """Get FEN representation of board."""
        pass
    
    @abstractmethod
    def is_checkmate(self, board: Any) -> bool:
        """Check if position is checkmate."""
        pass
    
    @abstractmethod
    def is_stalemate(self, board: Any) -> bool:
        """Check if position is stalemate."""
        pass


class ChessAI(ABC):
    """Interface for chess AI engines."""
    
    @abstractmethod
    def initialize(self, difficulty: int = 8, **kwargs) -> bool:
        """Initialize the AI engine."""
        pass
    
    @abstractmethod
    def get_best_move(self, board_state: Any, time_limit: float = 3.0) -> Optional[str]:
        """Get best move for current position."""
        pass
    
    @abstractmethod
    def evaluate_position(self, board_state: Any) -> Dict[str, Any]:
        """Evaluate current position."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up AI resources."""
        pass


class ComponentFactory:
    """Factory for creating pluggable components."""
    
    _validators = {}
    _board_states = {}
    _ais = {}
    
    @classmethod
    def register_validator(cls, name: str, validator_class):
        """Register a move validator implementation."""
        cls._validators[name] = validator_class
    
    @classmethod
    def register_board_state(cls, name: str, board_class):
        """Register a board state implementation."""
        cls._board_states[name] = board_class
    
    @classmethod
    def register_ai(cls, name: str, ai_class):
        """Register an AI implementation."""
        cls._ais[name] = ai_class
    
    @classmethod
    def create_validator(cls, name: str, **kwargs) -> ChessMoveValidator:
        """Create a move validator instance."""
        if name not in cls._validators:
            raise ValueError(f"Unknown validator: {name}")
        return cls._validators[name](**kwargs)
    
    @classmethod
    def create_board_state(cls, name: str, **kwargs) -> ChessBoardState:
        """Create a board state instance."""
        if name not in cls._board_states:
            raise ValueError(f"Unknown board state: {name}")
        return cls._board_states[name](**kwargs)
    
    @classmethod
    def create_ai(cls, name: str, **kwargs) -> ChessAI:
        """Create an AI instance."""
        if name not in cls._ais:
            raise ValueError(f"Unknown AI: {name}")
        return cls._ais[name](**kwargs)
    
    @classmethod
    def list_available(cls) -> Dict[str, List[str]]:
        """List all available implementations."""
        return {
            'validators': list(cls._validators.keys()),
            'board_states': list(cls._board_states.keys()),
            'ais': list(cls._ais.keys())
        }