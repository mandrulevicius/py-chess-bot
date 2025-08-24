"""Tests for position evaluation functionality."""

import pytest
from src.analysis.position_evaluator import get_position_evaluation, get_best_move_suggestion
from src.game.game_loop import create_game, make_move
from src.ai.stockfish_ai import create_ai, cleanup_ai


class TestPositionEvaluator:
    """Test position evaluation using existing Stockfish AI."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.game = create_game()
        self.ai = create_ai(difficulty=5)  # Low difficulty for speed
    
    def teardown_method(self):
        """Clean up test fixtures."""
        cleanup_ai(self.ai)
    
    def test_evaluate_starting_position(self):
        """Test evaluation of starting chess position."""
        evaluation = get_position_evaluation(self.game, self.ai)
        
        assert evaluation is not None
        assert 'score' in evaluation
        assert 'evaluation_type' in evaluation
        assert evaluation['evaluation_type'] in ['cp', 'mate', 'error']
        
        # Starting position should be roughly equal
        if evaluation['evaluation_type'] == 'cp':
            assert -50 <= evaluation['score'] <= 50  # Within reasonable range
    
    def test_evaluate_position_after_move(self):
        """Test evaluation after making a move."""
        # Make opening move
        game_after_e4 = make_move(self.game, 'e4')['new_game']
        
        evaluation = get_position_evaluation(game_after_e4, self.ai)
        
        assert evaluation is not None
        assert 'score' in evaluation
        assert 'evaluation_type' in evaluation
    
    def test_get_best_move_suggestion(self):
        """Test getting best move suggestion."""
        best_move = get_best_move_suggestion(self.game, self.ai)
        
        assert best_move is not None
        assert isinstance(best_move, str)
        assert len(best_move) >= 2  # At least 2 characters (e.g., 'e4')
        
        # Should be a legal move
        move_result = make_move(self.game, best_move)
        assert move_result['success'] is True
    
    def test_evaluation_with_invalid_game(self):
        """Test evaluation handles invalid game state gracefully."""
        # This should not crash, might return error evaluation
        invalid_game = None
        evaluation = get_position_evaluation(invalid_game, self.ai)
        
        # Should handle gracefully - either return error or raise appropriate exception
        if evaluation:
            assert 'evaluation_type' in evaluation
    
    def test_best_move_with_invalid_game(self):
        """Test best move suggestion handles invalid game gracefully."""
        invalid_game = None
        
        # Should handle gracefully - return None or raise appropriate exception
        try:
            result = get_best_move_suggestion(invalid_game, self.ai)
            # If it returns something, should be None for invalid input
            assert result is None or isinstance(result, str)
        except (ValueError, TypeError):
            # Expected to raise exception for invalid input
            pass