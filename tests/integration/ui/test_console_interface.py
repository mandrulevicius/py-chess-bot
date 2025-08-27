"""Tests for console interface functionality."""

import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from src.ui.console_interface import display_board, get_user_move, show_message, show_move_history


def test_display_board_starting_position():
    """Test displaying the starting chess position."""
    from src.game.game_loop import create_game
    
    game = create_game()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        display_board(game)
        output = fake_out.getvalue()
    
    # Should contain basic board representation
    assert "Turn 1:" in output
    assert "White to move" in output
    # Should show current position info
    assert len(output) > 50  # Some reasonable output length


def test_display_board_mid_game():
    """Test displaying a mid-game position."""
    from src.game.game_loop import create_game, make_move
    
    game = create_game()
    game = make_move(game, "e4")["new_game"]
    game = make_move(game, "e5")["new_game"]
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        display_board(game)
        output = fake_out.getvalue()
    
    assert "Turn 2:" in output
    assert "White to move" in output


def test_get_user_move_valid_input():
    """Test getting valid user move input."""
    with patch('builtins.input', return_value='e4'):
        move = get_user_move()
        assert move == 'e4'


def test_get_user_move_strips_whitespace():
    """Test that user input is cleaned up."""
    with patch('builtins.input', return_value='  Nf3  \n'):
        move = get_user_move()
        assert move == 'Nf3'


def test_get_user_move_empty_input():
    """Test handling empty input."""
    with patch('builtins.input', side_effect=['', '  ', 'e4']):
        move = get_user_move()
        assert move == 'e4'


def test_show_message():
    """Test displaying messages to user."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        show_message("Test message")
        output = fake_out.getvalue()
    
    assert "Test message" in output


def test_show_move_history():
    """Test displaying move history."""
    from src.game.game_loop import create_game, make_move
    
    game = create_game()
    game = make_move(game, "e4")["new_game"]
    game = make_move(game, "e5")["new_game"]
    game = make_move(game, "Nf3")["new_game"]
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        show_move_history(game)
        output = fake_out.getvalue()
    
    assert "Move History:" in output
    assert "1. e4 e5" in output
    assert "2. Nf3" in output


def test_show_game_status_active():
    """Test displaying active game status."""
    from src.ui.console_interface import show_game_status
    from src.game.game_loop import create_game
    
    game = create_game()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        show_game_status(game)
        output = fake_out.getvalue()
    
    assert "Game Status:" in output
    assert "Game in progress" in output


def test_show_legal_moves():
    """Test displaying available legal moves."""
    from src.ui.console_interface import show_legal_moves
    from src.game.game_loop import create_game
    
    game = create_game()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        show_legal_moves(game)
        output = fake_out.getvalue()
    
    assert "Legal moves:" in output
    assert "e4" in output
    assert "Nf3" in output


def test_show_error_message():
    """Test displaying error messages with special formatting."""
    from src.ui.console_interface import show_error
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        show_error("Invalid move: e9")
        output = fake_out.getvalue()
    
    assert "ERROR:" in output
    assert "Invalid move: e9" in output


def test_clear_screen():
    """Test screen clearing functionality."""
    from src.ui.console_interface import clear_screen
    
    # Test that subprocess.run is called, not os.system
    with patch('subprocess.run') as mock_subprocess:
        clear_screen()
        mock_subprocess.assert_called()


def test_display_welcome_message():
    """Test welcome message display."""
    from src.ui.console_interface import display_welcome
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        display_welcome()
        output = fake_out.getvalue()
    
    assert "PyChessBot" in output
    assert "Welcome" in output or "Chess" in output