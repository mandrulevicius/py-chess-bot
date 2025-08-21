"""Tests for PyGame GUI interface components."""

import pytest
from unittest.mock import Mock, patch
from src.ui.pygame_interface import MouseHandler, ChessboardRenderer, PieceAssets


class TestMouseHandler:
    """Test mouse handling and coordinate conversion."""
    
    def test_screen_to_board_coords_valid(self):
        """Test valid screen coordinate conversion."""
        # Test click in top-left square (a8)
        result = MouseHandler.screen_to_board_coords(100, 100)  # Within board bounds
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_screen_to_board_coords_invalid(self):
        """Test invalid screen coordinate conversion."""
        # Test click outside board
        result = MouseHandler.screen_to_board_coords(10, 10)  # Outside board
        assert result is None
    
    def test_board_coords_to_algebraic(self):
        """Test coordinate to algebraic notation conversion."""
        # Test a8 square (top-left)
        result = MouseHandler.board_coords_to_algebraic(0, 0)
        assert result == "a8"
        
        # Test e4 square
        result = MouseHandler.board_coords_to_algebraic(4, 4)
        assert result == "e4"
        
        # Test h1 square (bottom-right)
        result = MouseHandler.board_coords_to_algebraic(7, 7)
        assert result == "h1"


class TestChessboardRenderer:
    """Test chessboard rendering components (without actual rendering)."""
    
    def test_renderer_initialization(self):
        """Test renderer can be initialized."""
        mock_screen = Mock()
        renderer = ChessboardRenderer(mock_screen)
        
        assert renderer.screen == mock_screen
        assert renderer.selected_square is None
        assert renderer.legal_moves == []
    
    def test_set_selected_square(self):
        """Test setting selected square."""
        mock_screen = Mock()
        renderer = ChessboardRenderer(mock_screen)
        
        renderer.set_selected_square((3, 4))
        assert renderer.selected_square == (3, 4)
        
        renderer.set_selected_square(None)
        assert renderer.selected_square is None
    
    def test_set_legal_moves(self):
        """Test setting legal moves."""
        mock_screen = Mock()
        renderer = ChessboardRenderer(mock_screen)
        
        moves = [(1, 2), (3, 4), (5, 6)]
        renderer.set_legal_moves(moves)
        assert renderer.legal_moves == moves


class TestPieceAssets:
    """Test piece asset loading (without pygame)."""
    
    @patch('pygame.font.Font')
    @patch('pygame.font.SysFont')
    @patch('pygame.Surface')
    def test_piece_assets_initialization(self, mock_surface, mock_sysfont, mock_font):
        """Test piece assets can be initialized."""
        # Mock font rendering
        mock_font_obj = Mock()
        mock_rendered_surface = Mock()
        mock_rendered_surface.get_width.return_value = 20
        mock_rendered_surface.get_height.return_value = 20
        mock_font_obj.render.return_value = mock_rendered_surface
        mock_sysfont.return_value = mock_font_obj
        mock_font.return_value = mock_font_obj
        
        # Mock pygame Surface
        mock_surface.return_value = Mock()
        
        pieces = PieceAssets()
        
        # Should have pieces for both colors
        assert 'white' in pieces.pieces
        assert 'black' in pieces.pieces
        
        # Should have all piece types
        expected_pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        for piece_type in expected_pieces:
            assert piece_type in pieces.pieces['white']
            assert piece_type in pieces.pieces['black']
    
    @patch('pygame.font.Font')
    @patch('pygame.font.SysFont')
    @patch('pygame.Surface')
    def test_get_piece_surface(self, mock_surface, mock_sysfont, mock_font):
        """Test getting piece surfaces."""
        # Mock font rendering
        mock_font_obj = Mock()
        mock_rendered_surface = Mock()
        mock_rendered_surface.get_width.return_value = 20
        mock_rendered_surface.get_height.return_value = 20
        mock_font_obj.render.return_value = mock_rendered_surface
        mock_sysfont.return_value = mock_font_obj
        mock_font.return_value = mock_font_obj
        
        # Mock pygame Surface
        mock_surface.return_value = Mock()
        
        pieces = PieceAssets()
        
        # Test valid piece
        result = pieces.get_piece_surface('king', 'white')
        assert result is not None
        
        # Test invalid piece
        result = pieces.get_piece_surface('invalid', 'white')
        assert result is None
        
        # Test invalid color
        result = pieces.get_piece_surface('king', 'invalid')
        assert result is None


def test_pygame_interface_imports():
    """Test that pygame interface can be imported without errors."""
    try:
        from src.ui.pygame_interface import (
            ChessboardRenderer, PieceAssets, MouseHandler, GameGUI, run_gui_game
        )
        assert True  # If we get here, imports worked
    except ImportError:
        pytest.skip("PyGame not available")
    except Exception as e:
        pytest.fail(f"Unexpected error importing pygame interface: {e}")


def test_constants_defined():
    """Test that required constants are defined."""
    from src.ui.pygame_interface import (
        WINDOW_SIZE, BOARD_SIZE, SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y,
        WHITE_SQUARE, BLACK_SQUARE, BACKGROUND, TEXT_COLOR
    )
    
    # Basic sanity checks
    assert WINDOW_SIZE > 0
    assert BOARD_SIZE > 0
    assert SQUARE_SIZE > 0
    assert len(WHITE_SQUARE) == 3  # RGB tuple
    assert len(BLACK_SQUARE) == 3  # RGB tuple
    assert len(BACKGROUND) == 3   # RGB tuple
    assert len(TEXT_COLOR) == 3   # RGB tuple