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