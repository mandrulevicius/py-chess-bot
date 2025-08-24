"""Tests for move validation with board position."""

import pytest
from src.game.move_validator import validate_move


def test_validate_legal_opening_move():
    """Test validating a legal opening move."""
    # Starting position FEN
    starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    result = validate_move("e4", starting_position)
    
    assert result["valid"] is True
    assert result["legal"] is True
    assert result["piece"] == "pawn"
    assert result["destination"] == "e4"
    assert "move_object" in result


def test_validate_illegal_move_wrong_piece():
    """Test validating an illegal move - piece can't reach square."""
    starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    result = validate_move("Nf7", starting_position)  # Knight can't reach f7 from starting position
    
    assert result["valid"] is True  # Notation is valid
    assert result["legal"] is False  # But move is illegal
    assert result["piece"] == "knight"
    assert "error" in result


def test_validate_invalid_notation():
    """Test that invalid notation fails without checking legality."""
    starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    result = validate_move("X4", starting_position)
    
    assert result["valid"] is False
    assert "legal" not in result  # Shouldn't even check legality
    assert "error" in result


def test_validate_without_board_state():
    """Test that function works without board state (syntax only)."""
    result = validate_move("e4")  # No board position provided
    
    assert result["valid"] is True
    assert result["piece"] == "pawn"
    assert "legal" not in result  # No legality check without board
    assert "move_object" not in result


def test_validate_castling_legal():
    """Test validating legal castling."""
    # Position where white can castle kingside
    castling_position = "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 1"
    
    result = validate_move("O-O", castling_position)
    
    assert result["valid"] is True
    assert result["legal"] is True
    assert result["castling"] == "kingside"