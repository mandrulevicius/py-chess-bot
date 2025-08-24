"""Tests for basic chess game loop functionality."""

import pytest
from src.game.game_loop import create_game, make_move, get_game_status, get_current_player


def test_create_new_game():
    """Test creating a new chess game."""
    game = create_game()
    
    assert game is not None
    assert get_current_player(game) == "white"
    
    status = get_game_status(game)
    assert status["active"] is True
    assert status["winner"] is None
    assert status["turn_count"] == 1


def test_make_valid_opening_moves():
    """Test making valid opening moves alternating players."""
    game = create_game()
    
    # White plays e4
    result = make_move(game, "e4")
    assert result["success"] is True
    assert "new_game" in result
    
    game = result["new_game"]
    assert get_current_player(game) == "black"
    
    # Black plays e5
    result = make_move(game, "e5")
    assert result["success"] is True
    
    game = result["new_game"]
    assert get_current_player(game) == "white"
    
    status = get_game_status(game)
    assert status["turn_count"] == 2


def test_make_invalid_move():
    """Test making an invalid move doesn't change game state."""
    game = create_game()
    original_player = get_current_player(game)
    
    result = make_move(game, "e8")  # Invalid opening move
    
    assert result["success"] is False
    assert "error" in result
    assert "new_game" not in result
    # Original game should be unchanged
    assert get_current_player(game) == original_player


def test_game_immutability():
    """Test that making moves doesn't modify original game."""
    original_game = create_game()
    original_player = get_current_player(original_game)
    
    make_move(original_game, "e4")
    
    # Original game should be unchanged
    assert get_current_player(original_game) == original_player


def test_get_legal_moves_from_game():
    """Test getting legal moves from current game position."""
    from src.game.game_loop import get_legal_moves
    
    game = create_game()
    legal_moves = get_legal_moves(game)
    
    assert len(legal_moves) == 20  # 20 legal moves in starting position
    assert "e4" in legal_moves
    assert "Nf3" in legal_moves


def test_game_move_history():
    """Test tracking move history."""
    from src.game.game_loop import get_move_history
    
    game = create_game()
    
    # Make a few moves
    game = make_move(game, "e4")["new_game"]
    game = make_move(game, "e5")["new_game"] 
    game = make_move(game, "Nf3")["new_game"]
    
    history = get_move_history(game)
    assert len(history) == 3
    assert history[0] == "e4"
    assert history[1] == "e5"
    assert history[2] == "Nf3"


def test_create_game_from_position():
    """Test creating game from custom position."""
    custom_fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
    game = create_game(position=custom_fen)
    
    assert game is not None
    assert get_current_player(game) == "white"
    
    status = get_game_status(game)
    assert status["turn_count"] == 2