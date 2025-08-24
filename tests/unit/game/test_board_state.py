"""Tests for chess board state management."""

import pytest
from src.game.board_state import create_board, apply_move, get_board_fen


def test_create_starting_board():
    """Test creating a board in starting position."""
    board = create_board()
    
    assert board is not None
    fen = get_board_fen(board)
    expected_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert fen == expected_fen


def test_create_board_from_fen():
    """Test creating a board from custom FEN."""
    custom_fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
    board = create_board(custom_fen)
    
    assert board is not None
    assert get_board_fen(board) == custom_fen


def test_apply_legal_move():
    """Test applying a legal move to the board."""
    board = create_board()
    
    # Apply e4 opening move
    result = apply_move(board, "e4")
    
    assert result["success"] is True
    assert "new_board" in result
    
    # Check that position changed
    new_fen = get_board_fen(result["new_board"])
    expected_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    assert new_fen == expected_fen


def test_apply_illegal_move():
    """Test applying an illegal move returns error."""
    board = create_board()
    
    # Try to move king to e4 (illegal from starting position)
    result = apply_move(board, "Ke4")
    
    assert result["success"] is False
    assert "error" in result
    assert "new_board" not in result


def test_apply_invalid_notation():
    """Test applying invalid notation returns error."""
    board = create_board()
    
    result = apply_move(board, "X4")
    
    assert result["success"] is False
    assert "error" in result


def test_board_immutability():
    """Test that applying moves doesn't modify original board."""
    original_board = create_board()
    original_fen = get_board_fen(original_board)
    
    # Apply a move
    apply_move(original_board, "e4")
    
    # Original board should be unchanged
    assert get_board_fen(original_board) == original_fen


def test_get_legal_moves():
    """Test getting list of legal moves from position."""
    from src.game.board_state import get_legal_moves
    
    board = create_board()
    legal_moves = get_legal_moves(board)
    
    assert len(legal_moves) == 20  # 20 legal moves in starting position
    assert "e4" in legal_moves
    assert "Nf3" in legal_moves