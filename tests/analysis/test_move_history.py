"""Tests for move history and undo/redo functionality."""

import pytest
from src.analysis.move_history import (
    GameHistory, can_undo, can_redo, undo_move, redo_move, 
    get_current_position, get_move_count
)
from src.game.game_loop import create_game, make_move


class TestMoveHistory:
    """Test linear undo/redo move history system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.game = create_game()
        self.history = GameHistory()
        
        # Add starting position to history
        self.history.add_position(self.game)
    
    def test_create_empty_history(self):
        """Test creating empty game history."""
        history = GameHistory()
        
        assert history is not None
        assert can_undo(history) is False
        assert can_redo(history) is False
        assert get_move_count(history) == 0
    
    def test_add_starting_position(self):
        """Test adding starting position to history."""
        assert get_move_count(self.history) == 1
        assert can_undo(self.history) is False  # Can't undo from start
        assert can_redo(self.history) is False
        
        current = get_current_position(self.history)
        assert current is not None
    
    def test_add_moves_to_history(self):
        """Test adding moves creates proper history."""
        # Make some moves
        game1 = make_move(self.game, 'e4')['new_game']
        self.history.add_position(game1)
        
        game2 = make_move(game1, 'e5')['new_game'] 
        self.history.add_position(game2)
        
        assert get_move_count(self.history) == 3  # Start + 2 moves
        assert can_undo(self.history) is True
        assert can_redo(self.history) is False
    
    def test_undo_single_move(self):
        """Test undoing a single move."""
        # Make a move
        game1 = make_move(self.game, 'e4')['new_game']
        self.history.add_position(game1)
        
        # Undo the move
        success = undo_move(self.history)
        assert success is True
        
        # Should be back to starting position
        current = get_current_position(self.history)
        assert current is not None
        
        # Now we can redo but not undo further
        assert can_undo(self.history) is False
        assert can_redo(self.history) is True
    
    def test_redo_single_move(self):
        """Test redoing a move after undo."""
        # Make move, then undo it
        game1 = make_move(self.game, 'e4')['new_game']
        self.history.add_position(game1)
        undo_move(self.history)
        
        # Now redo the move
        success = redo_move(self.history)
        assert success is True
        
        # Should be back to position after e4
        current = get_current_position(self.history)
        assert current is not None
        
        # Should be able to undo but not redo
        assert can_undo(self.history) is True
        assert can_redo(self.history) is False
    
    def test_undo_multiple_moves(self):
        """Test undoing multiple moves in sequence."""
        # Make several moves
        games = [self.game]
        for move in ['e4', 'e5', 'Nf3', 'Nc6']:
            game = make_move(games[-1], move)['new_game']
            games.append(game)
            self.history.add_position(game)
        
        # Should have 5 positions total
        assert get_move_count(self.history) == 5
        
        # Undo 2 moves
        assert undo_move(self.history) is True
        assert undo_move(self.history) is True
        
        # Should be at position after e4, e5
        assert can_undo(self.history) is True
        assert can_redo(self.history) is True
    
    def test_new_move_after_undo_clears_redo(self):
        """Test that making a new move after undo clears the redo history."""
        # Make moves: e4, e5
        game1 = make_move(self.game, 'e4')['new_game']
        self.history.add_position(game1)
        
        game2 = make_move(game1, 'e5')['new_game']
        self.history.add_position(game2)
        
        # Undo back to after e4
        undo_move(self.history)
        assert can_redo(self.history) is True
        
        # Make a different move (d6)
        current = get_current_position(self.history)
        game3 = make_move(current, 'd6')['new_game']
        self.history.add_position(game3)
        
        # Should no longer be able to redo (e5 is lost)
        assert can_redo(self.history) is False
        assert can_undo(self.history) is True
    
    def test_undo_redo_edge_cases(self):
        """Test edge cases for undo/redo."""
        # Try to undo with no moves
        assert undo_move(self.history) is False
        
        # Try to redo with nothing to redo
        assert redo_move(self.history) is False
        
        # Make move, undo it, try to undo again
        game1 = make_move(self.game, 'e4')['new_game']
        self.history.add_position(game1)
        assert undo_move(self.history) is True
        assert undo_move(self.history) is False  # Already at start
        
        # Redo, then try to redo again
        assert redo_move(self.history) is True
        assert redo_move(self.history) is False  # Nothing more to redo
    
    def test_get_current_position(self):
        """Test getting current position from history."""
        current = get_current_position(self.history)
        assert current is not None
        
        # Make a move and check current changes
        game1 = make_move(self.game, 'e4')['new_game']
        self.history.add_position(game1)
        
        new_current = get_current_position(self.history)
        assert new_current is not None
        assert new_current != current  # Should be different position