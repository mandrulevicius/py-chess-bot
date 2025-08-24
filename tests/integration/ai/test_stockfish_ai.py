"""Tests for Stockfish AI integration."""

import pytest
from src.ai.stockfish_ai import create_ai, get_ai_move, set_ai_difficulty


def test_create_ai_default():
    """Test creating AI with default settings."""
    ai = create_ai()
    
    assert ai is not None
    assert ai["engine_type"] == "stockfish"
    assert ai["difficulty"] is not None


def test_create_ai_with_difficulty():
    """Test creating AI with specific difficulty level."""
    ai = create_ai(difficulty=5)
    
    assert ai is not None
    assert ai["difficulty"] == 5


def test_get_ai_move_opening():
    """Test getting AI move from starting position."""
    from src.game.game_loop import create_game
    
    ai = create_ai(difficulty=1)  # Low difficulty for predictable/fast response
    game = create_game()
    
    result = get_ai_move(ai, game)
    
    assert result["success"] is True
    assert "move" in result
    assert isinstance(result["move"], str)
    assert len(result["move"]) >= 2  # Valid SAN notation


def test_get_ai_move_mid_game():
    """Test getting AI move from mid-game position."""
    from src.game.game_loop import create_game, make_move
    
    ai = create_ai(difficulty=1)
    
    # Create a mid-game position
    game = create_game()
    game = make_move(game, "e4")["new_game"]
    game = make_move(game, "e5")["new_game"]
    game = make_move(game, "Nf3")["new_game"]
    
    result = get_ai_move(ai, game)
    
    assert result["success"] is True
    assert "move" in result
    assert result["move"] is not None


def test_ai_move_is_legal():
    """Test that AI only suggests legal moves."""
    from src.game.game_loop import create_game, get_legal_moves
    
    ai = create_ai(difficulty=1)
    game = create_game()
    
    legal_moves = get_legal_moves(game)
    result = get_ai_move(ai, game)
    
    assert result["success"] is True
    assert result["move"] in legal_moves


def test_set_ai_difficulty():
    """Test changing AI difficulty level."""
    ai = create_ai(difficulty=5)
    
    result = set_ai_difficulty(ai, 10)
    
    assert result["success"] is True
    assert "new_ai" in result
    assert result["new_ai"]["difficulty"] == 10


def test_invalid_difficulty_level():
    """Test handling invalid difficulty levels."""
    result_high = set_ai_difficulty(create_ai(), 25)  # Too high
    result_low = set_ai_difficulty(create_ai(), -5)   # Too low
    
    assert result_high["success"] is False
    assert "error" in result_high
    
    assert result_low["success"] is False
    assert "error" in result_low


def test_ai_engine_error_handling():
    """Test handling when Stockfish engine is not available."""
    # This test might be skipped if we can't simulate engine failure easily
    pytest.skip("Engine error simulation not implemented yet")


def test_ai_move_timeout():
    """Test AI move generation with time limits."""
    from src.game.game_loop import create_game
    
    ai = create_ai(difficulty=1)
    game = create_game()
    
    # This should complete quickly with low difficulty
    result = get_ai_move(ai, game, time_limit=2.0)
    
    assert result["success"] is True
    assert "move" in result