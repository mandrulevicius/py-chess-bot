"""Move history and undo/redo functionality."""

from typing import List, Optional, Any
import copy


class GameHistory:
    """Manages linear game history for undo/redo functionality."""
    
    def __init__(self):
        """Initialize empty game history."""
        self.positions: List[Any] = []
        self.current_index: int = -1  # Points to current position in history
    
    def add_position(self, game_state: Any) -> None:
        """
        Add a new position to the history.
        
        Args:
            game_state: Game state to add to history
        """
        # If we're in the middle of history (after undos), 
        # truncate the forward history and add new position
        self.positions = self.positions[:self.current_index + 1]
        
        # Add the new position
        self.positions.append(copy.deepcopy(game_state))
        self.current_index = len(self.positions) - 1
    
    def undo(self) -> bool:
        """
        Undo to previous position.
        
        Returns:
            True if undo was successful, False if no previous position
        """
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False
    
    def redo(self) -> bool:
        """
        Redo to next position.
        
        Returns:
            True if redo was successful, False if no next position
        """
        if self.current_index < len(self.positions) - 1:
            self.current_index += 1
            return True
        return False
    
    def get_current(self) -> Optional[Any]:
        """Get current position from history."""
        if 0 <= self.current_index < len(self.positions):
            return self.positions[self.current_index]
        return None
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self.current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self.current_index < len(self.positions) - 1
    
    def get_move_count(self) -> int:
        """Get total number of positions in history."""
        return len(self.positions)


# Module-level functions for convenience
def can_undo(history: GameHistory) -> bool:
    """Check if undo is possible."""
    return history.can_undo()


def can_redo(history: GameHistory) -> bool:
    """Check if redo is possible."""
    return history.can_redo()


def undo_move(history: GameHistory) -> bool:
    """Undo to previous position."""
    return history.undo()


def redo_move(history: GameHistory) -> bool:
    """Redo to next position."""
    return history.redo()


def get_current_position(history: GameHistory) -> Optional[Any]:
    """Get current position from history."""
    return history.get_current()


def get_move_count(history: GameHistory) -> int:
    """Get total number of positions in history."""
    return history.get_move_count()