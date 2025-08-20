"""Tests for move parsing functionality."""

import pytest
from src.game.move_parser import parse_san_move


def test_parse_basic_pawn_move():
    """Test parsing a basic pawn move."""
    result = parse_san_move("e4")
    
    assert result is not None
    assert result["piece"] == "pawn"
    assert result["destination"] == "e4"
    assert result["valid"] is True


def test_parse_piece_move():
    """Test parsing a piece move."""
    result = parse_san_move("Nf3")
    
    assert result is not None
    assert result["piece"] == "knight"
    assert result["destination"] == "f3"
    assert result["valid"] is True


def test_parse_invalid_notation():
    """Test parsing invalid notation returns error."""
    result = parse_san_move("X4")
    
    assert result is not None
    assert result["valid"] is False
    assert "error" in result


def test_parse_capture_moves():
    """Test parsing capture notation."""
    # Pawn capture
    result = parse_san_move("exd5")
    assert result["valid"] is True
    assert result["piece"] == "pawn"
    assert result["destination"] == "d5"
    assert result["capture"] is True
    
    # Piece capture
    result = parse_san_move("Nxf7")
    assert result["valid"] is True  
    assert result["piece"] == "knight"
    assert result["destination"] == "f7"
    assert result["capture"] is True


def test_parse_castling():
    """Test parsing castling notation."""
    # Kingside castling
    result = parse_san_move("O-O")
    assert result["valid"] is True
    assert result["castling"] == "kingside"
    
    # Queenside castling
    result = parse_san_move("O-O-O")
    assert result["valid"] is True
    assert result["castling"] == "queenside"


def test_parse_check_and_checkmate():
    """Test parsing check and checkmate notation."""
    # Check
    result = parse_san_move("Qh5+")
    assert result["valid"] is True
    assert result["piece"] == "queen"
    assert result["destination"] == "h5"
    assert result["check"] is True
    
    # Checkmate
    result = parse_san_move("Qf7#")
    assert result["valid"] is True
    assert result["piece"] == "queen"  
    assert result["destination"] == "f7"
    assert result["checkmate"] is True


def test_parse_pawn_promotion():
    """Test parsing pawn promotion notation."""
    result = parse_san_move("e8=Q")
    assert result["valid"] is True
    assert result["piece"] == "pawn"
    assert result["destination"] == "e8"
    assert result["promotion"] == "queen"


def test_parse_empty_and_invalid_input():
    """Test edge cases for invalid input."""
    # Empty string
    result = parse_san_move("")
    assert result["valid"] is False
    
    # None input
    result = parse_san_move(None)
    assert result["valid"] is False
    
    # Invalid square
    result = parse_san_move("e9")
    assert result["valid"] is False