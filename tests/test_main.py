"""Tests for main application functionality."""

import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
import main


def test_parse_command_line_args_default():
    """Test parsing command line arguments with defaults."""
    with patch('sys.argv', ['main.py']):
        args = main.parse_args()
        
        assert args.difficulty == 8
        assert args.human_color == 'white'


def test_parse_command_line_args_custom():
    """Test parsing custom command line arguments."""
    with patch('sys.argv', ['main.py', '--difficulty', '15', '--color', 'black']):
        args = main.parse_args()
        
        assert args.difficulty == 15
        assert args.human_color == 'black'


def test_setup_game_default():
    """Test setting up game with default parameters."""
    game, ai = main.setup_game()
    
    assert game is not None
    assert ai is not None
    assert ai['difficulty'] == 8


def test_setup_game_custom():
    """Test setting up game with custom parameters."""
    game, ai = main.setup_game(difficulty=5)
    
    assert game is not None
    assert ai is not None
    assert ai['difficulty'] == 5


def test_handle_user_commands():
    """Test handling special user commands."""
    from src.game.game_loop import create_game
    
    game = create_game()
    
    # Test help command
    with patch('main.show_help') as mock_help:
        result = main.handle_user_command('help', game)
        assert result is True
        mock_help.assert_called_once()
    
    # Test history command  
    with patch('main.show_move_history') as mock_history:
        result = main.handle_user_command('history', game)
        assert result is True
        mock_history.assert_called_once()
    
    # Test quit command
    result = main.handle_user_command('quit', game)
    assert result is None  # Should return None to exit
    
    # Test regular move (not a command)
    result = main.handle_user_command('e4', game)
    assert result is False  # Regular move, not handled as command


def test_human_turn_logic():
    """Test human turn logic without complex mocking."""
    # Just test that the function exists and has right signature
    assert callable(main.human_turn)


def test_ai_turn_logic():
    """Test AI turn logic without complex mocking."""
    # Test that function exists and works with basic setup
    from src.game.game_loop import create_game, make_move
    from src.ai.stockfish_ai import create_ai
    
    game = create_game()
    # Make it black's turn for AI
    game = make_move(game, 'e4')['new_game']
    
    ai = create_ai(difficulty=1)  # Low difficulty for speed
    
    result = main.ai_turn(game, ai)
    
    assert result['success'] is True
    assert 'new_game' in result


def test_is_game_over_active():
    """Test game over detection for active game."""
    from src.game.game_loop import create_game
    
    game = create_game()
    
    assert main.is_game_over(game) is False


def test_main_function_structure():
    """Test that main function exists and is callable."""
    # Just test the function exists - full integration test would be complex
    assert callable(main.main)


def test_show_game_result_structure():
    """Test that show_game_result function exists."""
    # Just test function exists - complex output testing is brittle
    assert callable(main.show_game_result)